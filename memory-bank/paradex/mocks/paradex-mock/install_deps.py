"""
Flask and WebSockets installation for Paradex mock servers.

pip install flask flask-cors
pip install websockets
"""

import sys
import subprocess

# Install dependencies
def install_dependencies():
    """Install required Python packages."""
    packages = ['flask', 'flask-cors', 'websockets']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")

if __name__ == '__main__':
    install_dependencies()
