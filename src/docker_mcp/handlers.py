from typing import List, Dict, Any
import asyncio
import os
import yaml
import platform
from python_on_whales import DockerClient
from mcp.types import TextContent, Tool, Prompt, PromptArgument, GetPromptResult, PromptMessage
from .docker_executor import DockerComposeExecutor
docker_client = DockerClient()


async def parse_port_mapping(host_key: str, container_port: str | int) -> tuple[str, str] | tuple[str, str, str]:
    if '/' in str(host_key):
        host_port, protocol = host_key.split('/')
        if protocol.lower() == 'udp':
            return (str(host_port), str(container_port), 'udp')
        return (str(host_port), str(container_port))

    if isinstance(container_port, str) and '/' in container_port:
        port, protocol = container_port.split('/')
        if protocol.lower() == 'udp':
            return (str(host_key), port, 'udp')
        return (str(host_key), port)

    return (str(host_key), str(container_port))


class DockerHandlers:
    TIMEOUT_AMOUNT = 200

    @staticmethod
    async def handle_create_container(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            image = arguments["image"]
            container_name = arguments.get("name")
            ports = arguments.get("ports", {})
            environment = arguments.get("environment", {})

            if not image:
                raise ValueError("Image name cannot be empty")

            port_mappings = []
            for host_key, container_port in ports.items():
                mapping = await parse_port_mapping(host_key, container_port)
                port_mappings.append(mapping)

            async def pull_and_run():
                if not docker_client.image.exists(image):
                    await asyncio.to_thread(docker_client.image.pull, image)

                container = await asyncio.to_thread(
                    docker_client.container.run,
                    image,
                    name=container_name,
                    publish=port_mappings,
                    envs=environment,
                    detach=True
                )
                return container

            container = await asyncio.wait_for(pull_and_run(), timeout=DockerHandlers.TIMEOUT_AMOUNT)
            return [TextContent(type="text", text=f"Created container '{container.name}' (ID: {container.id})")]
        except asyncio.TimeoutError:
            return [TextContent(type="text", text=f"Operation timed out after {DockerHandlers.TIMEOUT_AMOUNT} seconds")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating container: {str(e)} | Arguments: {arguments}")]

    @staticmethod
    async def handle_deploy_compose(arguments: Dict[str, Any]) -> List[TextContent]:
        debug_info = []
        try:
            compose_yaml = arguments.get("compose_yaml")
            compose_file = arguments.get("compose_file")
            project_name = arguments.get("project_name")

            if not project_name:
                raise ValueError("Missing required project_name")
            
            if not compose_yaml and not compose_file:
                raise ValueError("Either compose_yaml or compose_file must be provided")

            # Handle local file path
            if compose_file:
                if not os.path.exists(compose_file):
                    raise ValueError(f"Docker Compose file not found: {compose_file}")
                compose_path = compose_file
                debug_info.append(f"Using local compose file: {compose_file}")
                cleanup_needed = False
            else:
                # Handle inline YAML content
                yaml_content = DockerHandlers._process_yaml(
                    compose_yaml, debug_info)
                compose_path = DockerHandlers._save_compose_file(
                    yaml_content, project_name)
                cleanup_needed = True

            try:
                result = await DockerHandlers._deploy_stack(compose_path, project_name, debug_info)
                return [TextContent(type="text", text=result)]
            finally:
                if cleanup_needed:
                    DockerHandlers._cleanup_files(compose_path)

        except Exception as e:
            debug_output = "\n".join(debug_info)
            return [TextContent(type="text", text=f"Error deploying compose stack: {str(e)}\n\nDebug Information:\n{debug_output}")]

    @staticmethod
    def _process_yaml(compose_yaml: str, debug_info: List[str]) -> dict:
        debug_info.append("=== Original YAML ===")
        debug_info.append(compose_yaml)

        try:
            yaml_content = yaml.safe_load(compose_yaml)
            debug_info.append("\n=== Loaded YAML Structure ===")
            debug_info.append(str(yaml_content))
            return yaml_content
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")

    @staticmethod
    def _save_compose_file(yaml_content: dict, project_name: str) -> str:
        compose_dir = os.path.join(os.getcwd(), "docker_compose_files")
        os.makedirs(compose_dir, exist_ok=True)

        compose_yaml = yaml.safe_dump(
            yaml_content, default_flow_style=False, sort_keys=False)
        compose_path = os.path.join(
            compose_dir, f"{project_name}-docker-compose.yml")

        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_yaml)
            f.flush()
            if platform.system() != 'Windows':
                os.fsync(f.fileno())

        return compose_path

    @staticmethod
    async def _deploy_stack(compose_path: str, project_name: str, debug_info: List[str]) -> str:
        compose = DockerComposeExecutor(compose_path, project_name)

        for command in [compose.down, compose.up]:
            try:
                code, out, err = await command()
                debug_info.extend([
                    f"\n=== {command.__name__.capitalize()} Command ===",
                    f"Return Code: {code}",
                    f"Stdout: {out}",
                    f"Stderr: {err}"
                ])

                if code != 0 and command == compose.up:
                    raise Exception(f"Deploy failed with code {code}: {err}")
            except Exception as e:
                if command != compose.down:
                    raise e
                debug_info.append(f"Warning during {
                                  command.__name__}: {str(e)}")

        code, out, err = await compose.ps()
        service_info = out if code == 0 else "Unable to list services"

        return (f"Successfully deployed compose stack '{project_name}'\n"
                f"Running services:\n{service_info}\n\n"
                f"Debug Info:\n{chr(10).join(debug_info)}")

    @staticmethod
    def _cleanup_files(compose_path: str) -> None:
        try:
            if os.path.exists(compose_path):
                os.remove(compose_path)
            compose_dir = os.path.dirname(compose_path)
            if os.path.exists(compose_dir) and not os.listdir(compose_dir):
                os.rmdir(compose_dir)
        except Exception as e:
            print(f"Warning during cleanup: {str(e)}")

    @staticmethod
    async def handle_get_logs(arguments: Dict[str, Any]) -> List[TextContent]:
        debug_info = []
        try:
            container_name = arguments.get("container_name")
            if not container_name:
                raise ValueError("Missing required container_name")

            debug_info.append(f"Fetching logs for container '{
                              container_name}'")
            logs = await asyncio.to_thread(docker_client.container.logs, container_name, tail=100)

            return [TextContent(type="text", text=f"Logs for container '{container_name}':\n{logs}\n\nDebug Info:\n{chr(10).join(debug_info)}")]
        except Exception as e:
            debug_output = "\n".join(debug_info)
            return [TextContent(type="text", text=f"Error retrieving logs: {str(e)}\n\nDebug Information:\n{debug_output}")]

    @staticmethod
    async def handle_list_containers(arguments: Dict[str, Any] | None) -> List[TextContent]:
        debug_info = []
        try:
            show_all = True if not arguments else arguments.get("all", True)
            debug_info.append(f"Listing Docker containers (all={show_all})")
            
            containers = await asyncio.to_thread(docker_client.container.list, all=show_all)
            
            container_info = []
            for c in containers:
                ports = []
                if hasattr(c, 'ports') and c.ports:
                    for port_mapping in c.ports.items():
                        ports.append(f"{port_mapping[0]}->{port_mapping[1]}")
                ports_str = ", ".join(ports) if ports else "No ports"
                
                status = c.state.status
                if status == "running" and hasattr(c.state, 'started_at'):
                    status = f"Up {c.state.running_for}" if hasattr(c.state, 'running_for') else "Running"
                elif status == "exited":
                    status = f"Exited ({c.state.exit_code})"
                
                info = f"• {c.name} ({c.id[:12]})\n  Image: {c.config.image}\n  Status: {status}\n  Ports: {ports_str}"
                container_info.append(info)
            
            result = "\n\n".join(container_info) if container_info else "No containers found"
            
            return [TextContent(type="text", text=f"Docker Containers:\n\n{result}")]
        except Exception as e:
            debug_output = "\n".join(debug_info)
            return [TextContent(type="text", text=f"Error listing containers: {str(e)}\n\nDebug Information:\n{debug_output}")]

    @staticmethod
    async def handle_stop_container(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            container_name = arguments.get("container_name")
            if not container_name:
                raise ValueError("Missing required container_name")
            
            container = await asyncio.to_thread(docker_client.container.get, container_name)
            await asyncio.to_thread(container.stop)
            
            return [TextContent(type="text", text=f"Successfully stopped container '{container_name}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error stopping container: {str(e)}")]

    @staticmethod
    async def handle_start_container(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            container_name = arguments.get("container_name")
            if not container_name:
                raise ValueError("Missing required container_name")
            
            container = await asyncio.to_thread(docker_client.container.get, container_name)
            await asyncio.to_thread(container.start)
            
            return [TextContent(type="text", text=f"Successfully started container '{container_name}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error starting container: {str(e)}")]

    @staticmethod
    async def handle_remove_container(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            container_name = arguments.get("container_name")
            force = arguments.get("force", False)
            
            if not container_name:
                raise ValueError("Missing required container_name")
            
            container = await asyncio.to_thread(docker_client.container.get, container_name)
            
            # Check if container is running and force is not set
            if container.state.status == "running" and not force:
                return [TextContent(type="text", text=f"Container '{container_name}' is running. Use force=true to remove it, or stop it first.")]
            
            await asyncio.to_thread(container.remove, force=force)
            
            return [TextContent(type="text", text=f"Successfully removed container '{container_name}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error removing container: {str(e)}")]

    @staticmethod
    async def handle_list_images(arguments: Dict[str, Any] | None) -> List[TextContent]:
        try:
            images = await asyncio.to_thread(docker_client.image.list)
            
            image_info = []
            for img in images:
                # Get tags
                tags = img.repo_tags if hasattr(img, 'repo_tags') else []
                tag_str = ", ".join(tags) if tags else "<none>"
                
                # Get size
                size_mb = img.size / (1024 * 1024) if hasattr(img, 'size') else 0
                size_str = f"{size_mb:.1f}MB"
                
                # Get created time
                created = img.attrs.get('Created', 'Unknown') if hasattr(img, 'attrs') else 'Unknown'
                
                info = f"• {tag_str}\n  ID: {img.id[:12]}\n  Size: {size_str}\n  Created: {created}"
                image_info.append(info)
            
            result = "\n\n".join(image_info) if image_info else "No images found"
            
            return [TextContent(type="text", text=f"Docker Images:\n\n{result}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing images: {str(e)}")]

    @staticmethod
    async def handle_pull_image(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            image = arguments.get("image")
            if not image:
                raise ValueError("Missing required image name")
            
            # Pull the image
            result = await asyncio.to_thread(docker_client.image.pull, image)
            
            return [TextContent(type="text", text=f"Successfully pulled image '{image}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error pulling image: {str(e)}")]

    @staticmethod
    async def handle_remove_image(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            image = arguments.get("image")
            force = arguments.get("force", False)
            
            if not image:
                raise ValueError("Missing required image name or ID")
            
            # Remove the image
            await asyncio.to_thread(docker_client.image.remove, image, force=force)
            
            return [TextContent(type="text", text=f"Successfully removed image '{image}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error removing image: {str(e)}")]

    @staticmethod
    async def handle_list_volumes(arguments: Dict[str, Any] | None) -> List[TextContent]:
        try:
            filters = arguments.get("filters", {}) if arguments else {}
            
            volumes = await asyncio.to_thread(docker_client.volume.list, filters=filters)
            
            volume_info = []
            for vol in volumes:
                # Get volume details
                name = vol.name if hasattr(vol, 'name') else 'Unknown'
                driver = vol.driver if hasattr(vol, 'driver') else 'local'
                mountpoint = vol.mountpoint if hasattr(vol, 'mountpoint') else 'Unknown'
                
                # Get labels
                labels = vol.labels if hasattr(vol, 'labels') else {}
                label_str = ", ".join([f"{k}={v}" for k, v in labels.items()]) if labels else "No labels"
                
                # Get scope
                scope = vol.scope if hasattr(vol, 'scope') else 'local'
                
                info = f"• {name}\n  Driver: {driver}\n  Scope: {scope}\n  Mountpoint: {mountpoint}\n  Labels: {label_str}"
                volume_info.append(info)
            
            result = "\n\n".join(volume_info) if volume_info else "No volumes found"
            
            return [TextContent(type="text", text=f"Docker Volumes:\n\n{result}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing volumes: {str(e)}")]

    @staticmethod
    async def handle_remove_volume(arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            volume_name = arguments.get("volume_name")
            force = arguments.get("force", False)
            
            if not volume_name:
                raise ValueError("Missing required volume_name")
            
            # Remove the volume
            await asyncio.to_thread(docker_client.volume.remove, volume_name, force=force)
            
            return [TextContent(type="text", text=f"Successfully removed volume '{volume_name}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error removing volume: {str(e)}")]
