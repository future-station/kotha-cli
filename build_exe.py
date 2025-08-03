#!/usr/bin/env python3
"""
Kotha CLI Standalone Executable Builder

This script creates a standalone executable that can run on machines
without Python installed.
"""

import subprocess
import sys
import os
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
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return None

def clean_build_dirs():
    """Clean build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__", "kotha/__pycache__"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"🧹 Cleaning {dir_name}/")
            shutil.rmtree(dir_path)

def main():
    """Main build function."""
    print("🏗️  Kotha CLI Standalone Executable Builder")
    print("=" * 60)

    # Check if Python is available
    python_cmd = "python" if os.name == 'nt' else "python3"

    result = run_command(f"{python_cmd} --version", "Checking Python installation")
    if not result:
        print("❌ Python is not installed or not in PATH.")
        return False

    print(f"📍 Using Python: {result.stdout.strip()}")

    # Clean previous builds
    clean_build_dirs()

    # Install PyInstaller if not already installed
    result = run_command(f"{python_cmd} -m pip install pyinstaller", "Installing PyInstaller")
    if not result:
        print("❌ Failed to install PyInstaller")
        return False

    # Create the executable
    pyinstaller_cmd = (
        f"{python_cmd} -m PyInstaller "
        "--onefile "
        "--console "
        "--name kotha "
        "--add-data \"kotha;kotha\" "
        "--hidden-import moviepy.video.io.VideoFileClip "
        "--hidden-import google.generativeai "
        "--hidden-import tqdm "
        "--hidden-import click "
        "--hidden-import python-dotenv "
        "--hidden-import pathlib "
        "--hidden-import json "
        "kotha/main.py"
    )

    result = run_command(pyinstaller_cmd, "Building standalone executable")
    if not result:
        print("❌ Failed to build executable")
        return False

    # Check if executable was created
    exe_path = Path("dist/kotha.exe")
    if exe_path.exists():
        print(f"\n🎉 Executable created successfully!")
        print(f"📍 Location: {exe_path.absolute()}")
        print(f"📏 Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")

        # Test the executable
        result = run_command("dist\\kotha.exe --version", "Testing executable")
        if result:
            print("✅ Executable test successful!")
        else:
            print("⚠️  Executable created but test failed")
    else:
        print("❌ Executable was not created")
        return False

    print("\n📖 Next steps:")
    print("1. Copy dist/kotha.exe to your target machine")
    print("2. Add the directory containing kotha.exe to PATH (optional)")
    print("3. Set API key: kotha.exe --set-api=\"your-api-key\"")
    print("4. Use: kotha.exe your-video.mp4")

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
