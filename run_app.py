"""
Launcher script for the Fake News Detection Web Application.
This script provides an easy way to run the application from the project root.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the Fake News Detection Web Application."""
    # Get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # Path to the app run script
    app_script = project_root / "src" / "app" / "run.py"
    
    # Create necessary directories if they don't exist
    os.makedirs(project_root / "data" / "processed", exist_ok=True)
    os.makedirs(project_root / "models", exist_ok=True)
    
    # Check if the app script exists
    if not app_script.exists():
        print(f"Error: Application script not found at {app_script}")
        sys.exit(1)
    
    # Information message
    print("=" * 80)
    print("Fake News Detection System")
    print("=" * 80)
    print("Starting web application...")
    print("Once started, you can access the application at http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    print("=" * 80)
    
    # Run the application
    try:
        # Execute the app script
        subprocess.run([sys.executable, str(app_script)], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\nError running application: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
