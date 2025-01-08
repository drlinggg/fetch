import os
import sys
from pathlib import Path

def remove_symlink():
    home_bin = Path.home() / ".local" / "bin"
    symlink_path = home_bin / "fetch"

    if symlink_path.exists() or symlink_path.is_symlink():
        symlink_path.unlink()
        print(f"Symlink removed: {symlink_path}")
    else:
        print(f"No symlink found at: {symlink_path}")

def main():
    try:
        remove_symlink()
        
        wrapper_script = Path.home() / ".local" / "bin" / "fetch"
        if wrapper_script.exists():
            wrapper_script.unlink()
            print(f"Wrapper script removed: {wrapper_script}")
        else:
            print(f"No wrapper script found at: {wrapper_script}")

        print("Uninstall finished.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
