import os
import subprocess
from google.genai import types

schema_run_python_file= types.FunctionDeclaration(
            name="run_python_file",
            description="Runs the specified program returned by the valid file, passing any optional argument alongside it",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The file path where the function being called exists",
                    ),
                    "args": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                        description="None by default. Otherwise specifies additional arguments in a list which will append to the function parameters being passed.",
                    ),
                },
            ),
        )

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        valid_file_path = os.path.isfile(target_file)
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not valid_file_path:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            cwd=working_dir_abs,
            timeout=30,
            )
            
        lines = []
        if result.returncode != 0:
            lines.append(f"Process exited with code {result.returncode}")
        if result.stdout:
            lines.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            lines.append(f"STDERR: {result.stderr}")
        if not result.stdout and not result.stderr:
            lines.append("No output produced")
        return "\n".join(lines)
    

    except subprocess.TimeoutExpired:
        return f"Error: process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"