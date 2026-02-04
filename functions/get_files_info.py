#THis file will stop the LLM from reading all the internal files of the PC

import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(target_dir)
        return_string = []
        for file in contents:
            size = os.path.getsize(os.path.join(target_dir, file))
            is_dir = os.path.isdir(os.path.join(target_dir, file))
            result = f"- {file}: file_size={size} bytes, is_dir={is_dir}"
            return_string.append(result)

        return "\n".join(return_string)
    except Exception as e:
        return f"Error: {e}"



