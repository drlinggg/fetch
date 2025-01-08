import os
import sys
import subprocess
from pathlib import Path

def get_executable_path():
    venv_path = subprocess.run(
        ["poetry", "env", "info", "--path"],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()
    
    executable_name = "fetch" 
    executable_path = Path(venv_path) / "bin" / executable_name
    
    return executable_path

def create_symlink(executable_path):
    home_bin = Path.home() / ".local" / "bin"
    home_bin.mkdir(parents=True, exist_ok=True)
    
    symlink_path = home_bin / executable_path.name

    if symlink_path.exists() or symlink_path.is_symlink():
        symlink_path.unlink()

    symlink_path.symlink_to(executable_path)
    print(f"Symlink created: {symlink_path}")

def main():
    try:
        executable_path = get_executable_path()
        create_symlink(executable_path)
        
        wrapper_script = Path.home() / ".local" / "bin" / "fetch"
        with open(wrapper_script, 'w') as f:
            f.write(f"""#!/usr/bin/env python
import sys
import os

sys.path.insert(0, '{os.path.abspath(Path(__file__).parent.parent)}')

from src.fetch import main

if __name__ == '__main__':
    sys.exit(main())
""")
        
        wrapper_script.chmod(0o755)

        print("Finished.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

