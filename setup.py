#!/usr/bin/env python3
"""
TruthLens AI Setup Script
Automated setup for the multilingual fake news detection system
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print the TruthLens AI banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔍 TruthLens AI Setup                     ║
    ║              Multilingual Fake News Detection               ║
    ║                                                              ║
    ║  🇮🇳 10 Indian Languages + 13 International Languages       ║
    ║  🤖 Powered by Google Gemini 2.0 Flash                     ║
    ║  📱 Fully Responsive Mobile Design                          ║
    ║  🔊 Text-to-Speech Support                                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Please run: pip install -r requirements.txt")
        sys.exit(1)

def check_api_key():
    """Check if Gemini API key is configured"""
    print("\n🔑 Checking API configuration...")
    
    # Read app.py to check for API key
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'AIzaSyCBv8jNE-5K8Ojs0UumdeBL_Zba68b4e18' in content:
                print("⚠️  Warning: Using default API key")
                print("   Please update the API key in app.py for production use")
                print("   Get your key from: https://ai.google.dev")
            else:
                print("✅ Custom API key configured")
    except FileNotFoundError:
        print("❌ app.py not found")
        sys.exit(1)

def create_run_script():
    """Create a simple run script"""
    print("\n📝 Creating run script...")
    
    script_content = """#!/bin/bash
# TruthLens AI Run Script

echo "🚀 Starting TruthLens AI..."
echo "📱 Open http://localhost:5001 in your browser"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 app.py
"""
    
    with open('run.sh', 'w') as f:
        f.write(script_content)
    
    # Make it executable on Unix systems
    if platform.system() != 'Windows':
        os.chmod('run.sh', 0o755)
    
    print("✅ Created run.sh script")

def print_instructions():
    """Print final instructions"""
    instructions = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎉 Setup Complete!                       ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  🚀 To start the application:                               ║
    ║     python3 app.py                                          ║
    ║     OR                                                       ║
    ║     ./run.sh                                                 ║
    ║                                                              ║
    ║  🌐 Open in browser:                                        ║
    ║     http://localhost:5001                                    ║
    ║                                                              ║
    ║  📚 Documentation:                                          ║
    ║     README.md                                                ║
    ║     test_examples.md                                         ║
    ║                                                              ║
    ║  🧪 Test Examples:                                          ║
    ║     Hindi: तत्काल: नासा ने पुष्टि की है...                    ║
    ║     Tamil: அதிர்ச்சி: நாசா உறுதிப்படுத்தியுள்ளது...           ║
    ║     English: Breaking: NASA confirms...                     ║
    ║                                                              ║
    ║  🔧 Features:                                               ║
    ║     • 23 Languages (10 Indian + 13 International)          ║
    ║     • Text & Image Analysis                                  ║
    ║     • Text-to-Speech                                         ║
    ║     • Mobile Responsive                                      ║
    ║     • Cyber-themed UI                                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(instructions)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Check API key
    check_api_key()
    
    # Create run script
    create_run_script()
    
    # Print final instructions
    print_instructions()

if __name__ == "__main__":
    main()
