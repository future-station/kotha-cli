#!/usr/bin/env python3
"""
Kotha CLI Installer Script

This script installs the Kotha CLI tool globally on your system.
After installation, you can use the 'kotha' command from anywhere.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return None

def main():
    """Main installation function."""
    print("🎥 Kotha CLI Installer")
    print("=" * 50)

    # Check if Python is available
    python_cmd = "python" if os.name == 'nt' else "python3"

    result = run_command(f"{python_cmd} --version", "Checking Python installation")
    if not result:
        print("❌ Python is not installed or not in PATH.")
        print("   Please install Python 3.8+ from https://python.org")
        return False

    print(f"📍 Using Python: {result.stdout.strip()}")

    # Install the package
    install_cmd = f"{python_cmd} -m pip install kotha-cli"
    result = run_command(install_cmd, "Installing Kotha CLI")
    if not result:
        print("❌ Failed to install Kotha CLI")
        return False

    # Test the installation
    result = run_command("kotha --version", "Testing installation")
    if not result:
        print("❌ Installation verification failed")
        print("   The 'kotha' command is not available in PATH")
        print("   You may need to restart your terminal or add Python scripts to PATH")
        return False

    print("\n🎉 Installation completed successfully!")
    print("\n📖 Next steps:")
    print("1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Set your API key: kotha --set-api=\"your-api-key-here\"")
    print("3. Start using: kotha your-video.mp4")
    print("\n💡 For help: kotha --help")

    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
