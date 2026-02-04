import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        # 1. Path resolution
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # 2. Security: Path Traversal Protection
        # Updated error message to match your test requirement: "Cannot execute..."
        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 3. Validation: Existence and Extension
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 4. Command Construction
        python_args = args if args is not None else []
        command = ["python", target_path] + python_args

        # 5. Execution
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 6. Output Formatting
        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        if result.returncode != 0:
            return f"Process exited with return code {result.returncode}\n{output}"

        return output if (result.stdout or result.stderr) else "No output produced"

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error executing Python file: {e}"