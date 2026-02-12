import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Reads file content. Takes the path of the file being read.",
            parameters=types.Schema(
                required=["file_path"],
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Reads file content. Takes the path of the file being read.",
                    ),
                },
            ),
        )

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000
        with open(target_file, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: Can not read files: {e}"
