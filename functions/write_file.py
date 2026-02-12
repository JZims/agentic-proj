import os 
from google.genai import types

schema_write_file= types.FunctionDeclaration(
            name="write_file",
            description="Writes r",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                required=["file_path", "content"],
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path of the file being written to. A file with this name is created if it does not exist already.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="String content to be written into the given file",
                    ),
                },
            ),
        )

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        parent_dir = os.path.dirname(target_file)
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        if parent_dir and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Can not write files: {e}"
