#!/usr/bin/env python3
"""
Build script for Kotha CLI
Creates distribution packages for PyPI upload
"""

import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Error: {e.stderr}")
        return None

def clean_build_dirs():
    """Clean build directories."""
    dirs_to_clean = ["build", "dist", "kotha_cli.egg-info"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"🧹 Cleaning {dir_name}/")
            shutil.rmtree(dir_path)

def main():
    """Main build function."""
    print("🏗️  Kotha CLI Build Script")
    print("=" * 50)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Install/upgrade build tools
    result = run_command("python -m pip install --upgrade build twine", "Installing build tools")
    if not result:
        return False
    
    # Build the package
    result = run_command("python -m build", "Building package")
    if not result:
        return False
    
    # Check the package
    result = run_command("python -m twine check dist/*", "Checking package")
    if not result:
        return False
    
    print("\n🎉 Build completed successfully!")
    print("\n📦 Distribution files created in dist/:")
    
    dist_path = Path("dist")
    if dist_path.exists():
        for file in dist_path.iterdir():
            print(f"   - {file.name}")
    
    print("\n📖 Next steps:")
    print("1. Test the package: pip install dist/kotha_cli-*.whl")
    print("2. Upload to PyPI: python -m twine upload dist/*")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
