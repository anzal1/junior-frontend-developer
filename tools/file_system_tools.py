# tools/file_system_tools.py
import os


def write_react_component(file_path: str, code: str, project_path: str) -> str:
    """Writes a React component file within the specified project's 'src' directory."""
    clean_file_path = file_path.strip()

    if not clean_file_path.startswith("src/"):
        clean_file_path = os.path.join("src", clean_file_path)

    try:
        full_path = os.path.join(project_path, clean_file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(code)
        return f"Successfully wrote component to {clean_file_path}"
    except Exception as e:
        return f"Error writing file: {e}"


write_react_component_tool_def = {
    "type": "function",
    "function": {
        "name": "write_react_component",
        "description": "Writes or overwrites a React component file (.tsx) inside the project's 'src' directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The relative path from the 'src' directory. E.g., 'components/MyComponent.tsx' or 'App.tsx'."},
                "code": {"type": "string", "description": "The complete, well-formed React/TSX code for the component."},
                "project_path": {"type": "string", "description": "The root path of the project workspace."}
            }, "required": ["file_path", "code", "project_path"]
        }
    }
}
