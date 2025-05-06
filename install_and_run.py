"""
Installation and launcher script for the Fake News Detection Web Application.
This script installs the required dependencies and then runs the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required Python packages from requirements.txt."""
    # Get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # Path to the requirements file
    req_file = project_root / "requirements.txt"
    
    # Check if the requirements file exists
    if not req_file.exists():
        print(f"Error: Requirements file not found at {req_file}")
        print("Creating minimal requirements file...")
        
        # Create a minimal requirements file
        minimal_requirements = """
flask==2.3.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
nltk==3.8.1
textblob==0.17.1
textstat==0.7.3
pyyaml==6.0.1
"""
        with open(req_file, 'w') as f:
            f.write(minimal_requirements.strip())
    
    # Install the requirements
    print("=" * 80)
    print("Installing required packages...")
    print("This may take a few minutes depending on your internet connection.")
    print("=" * 80)
    
    try:
        # Use pip to install the requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)], check=True)
        print("\nAll packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing packages: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error during installation: {e}")
        return False

def setup_nltk():
    """Download required NLTK resources."""
    print("Downloading NLTK resources...")
    
    try:
        import nltk
        
        # Download essential NLTK resources
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('vader_lexicon')
        
        print("NLTK resources downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")
        return False

def create_minimal_application():
    """Create a minimal version of the application if the full one fails."""
    # Get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # Path to the simplified app
    simple_app_dir = project_root / "simple_app"
    os.makedirs(simple_app_dir, exist_ok=True)
    
    # Create a simple Flask application
    app_py = """from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = 'fake_news_detection_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.form.get('content', '')
    title = request.form.get('title', '')
    
    # Simple keyword-based analysis
    fake_keywords = [
        'conspiracy', 'shocking', 'they don\\'t want you to know', 
        'secret', 'cover-up', 'hoax', 'scam', 'miracle', 'cure',
        'controversial', 'anonymous', 'whistleblower', 'hidden',
        'government', 'exposed', 'shocking truth', 'censored'
    ]
    
    # Count fake news keywords
    content_lower = content.lower()
    keyword_count = sum(1 for keyword in fake_keywords if keyword.lower() in content_lower)
    
    # Calculate probability based on keyword count and text length
    fake_prob = min(0.9, keyword_count * 0.2)  # Cap at 0.9
    
    # Adjust based on text length (short texts with keywords are more suspicious)
    if len(content.split()) < 50 and keyword_count > 0:
        fake_prob = max(fake_prob, 0.7)
    
    # Add some randomness for demonstration
    fake_prob = min(0.95, max(0.05, fake_prob + (random.random() - 0.5) * 0.1))
    
    # Determine result
    if fake_prob >= 0.7:
        result = "Likely Fake"
        confidence = "High"
    elif fake_prob >= 0.4:
        result = "Possibly Fake"
        confidence = "Medium"
    else:
        result = "Likely Real"
        confidence = "High"
    
    result_data = {
        "result": result,
        "confidence": confidence,
        "fake_probability": fake_prob,
        "real_probability": 1 - fake_prob,
        "timestamp": "2023-05-06T12:00:00"
    }
    
    return render_template('result.html', 
                          content=content,
                          title=title,
                          source=request.form.get('source', ''),
                          result=result_data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    
    # Create the app.py file
    with open(simple_app_dir / "app.py", 'w') as f:
        f.write(app_py)
    
    # Create templates directory
    templates_dir = simple_app_dir / "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Copy template files from the main app
    for template in ["base.html", "index.html", "result.html", "about.html"]:
        src_path = project_root / "src" / "app" / "templates" / template
        if src_path.exists():
            with open(src_path, 'r') as src_file:
                content = src_file.read()
                
            with open(templates_dir / template, 'w') as dest_file:
                dest_file.write(content)
        else:
            print(f"Warning: Template file {template} not found")
    
    print(f"Minimal application created at {simple_app_dir}")
    return simple_app_dir / "app.py"

def run_app():
    """Run the Fake News Detection Web Application."""
    # Get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # Path to the app run script
    app_script = project_root / "src" / "app" / "run.py"
    
    # Create necessary directories if they don't exist
    os.makedirs(project_root / "data" / "processed", exist_ok=True)
    os.makedirs(project_root / "models", exist_ok=True)
    
    # Information message
    print("=" * 80)
    print("Fake News Detection System")
    print("=" * 80)
    print("Starting web application...")
    print("Once started, you can access the application at http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    print("=" * 80)
    
    # Try to run the main application
    try:
        # Check if the app script exists
        if app_script.exists():
            # Execute the app script
            subprocess.run([sys.executable, str(app_script)], check=True)
        else:
            print(f"Warning: Application script not found at {app_script}")
            
            # Try to run the simplified application
            simple_app = create_minimal_application()
            subprocess.run([sys.executable, str(simple_app)], check=True)
            
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\nError running application: {e}")
        
        # Try to run the simplified application
        try:
            print("\nTrying to run simplified application...")
            simple_app = create_minimal_application()
            subprocess.run([sys.executable, str(simple_app)], check=True)
        except Exception as se:
            print(f"\nError running simplified application: {se}")
            
    except Exception as e:
        print(f"\nUnexpected error: {e}")

def main():
    """Main function to install requirements and run the app."""
    print("=" * 80)
    print("Fake News Detection System - Setup and Launch")
    print("=" * 80)
    
    # Install requirements
    if install_requirements():
        # Setup NLTK resources
        setup_nltk()
        
        # Run the application
        run_app()
    else:
        print("\nFailed to install required packages. Cannot start the application.")
        print("Please try to install the packages manually:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
