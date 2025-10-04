# tools/shell_tools.py
import subprocess
import os


def execute_shell_command(command: str, cwd_override: str = None) -> str:
    """Executes a shell command in a specified directory or the project root."""
    working_dir = cwd_override if cwd_override else "."

    if not os.path.exists(working_dir):
        return f"Error: Working directory '{working_dir}' does not exist. Cannot run command."

    try:
        print(f"Executing command: `{command}` in directory: `{working_dir}`")
        result = subprocess.run(
            command, shell=True, check=True, cwd=working_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output = f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        return f"Command '{command}' executed successfully.\n{output}"
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}'. Return code: {e.returncode}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


execute_shell_tool_def = {
    "type": "function",
    "function": {
        "name": "execute_shell_command",
        "description": "Executes a shell command. Can override the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to be executed."},
                "cwd_override": {"type": "string", "description": "Optional. The directory to run the command in. Defaults to project root."}
            },
            "required": ["command"]
        }
    }
}
