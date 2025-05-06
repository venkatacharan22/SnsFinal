"""
Simple Fake News Detection Web Application using Flask.
This version uses a basic keyword-based approach without complex dependencies.
"""

from flask import Flask, render_template_string, request
import random
import re
import os
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'fake_news_detection_secret_key'

# HTML Templates as strings
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake News Detection</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f7f9fc;
            color: #495057;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        main {
            flex-grow: 1;
        }
        
        .footer {
            margin-top: auto;
        }
        
        .card {
            border: none;
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
        }
        
        .progress {
            border-radius: 1rem;
            height: 1.5rem;
        }
        
        .progress-bar {
            font-weight: 600;
            transition: width 1s ease;
        }
        
        .result-card {
            transition: transform 0.3s ease-in-out;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
        }
        
        .content-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.25rem;
            padding: 1rem;
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-search-dollar me-2"></i>Fake News Detector
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer bg-light py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">© 2025 Fake News Detection System | <a href="/about">About</a></p>
        </div>
    </footer>

    <!-- Bootstrap JS and dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Animate progress bars on result page
        document.addEventListener('DOMContentLoaded', function() {
            const progressBars = document.querySelectorAll('.progress-bar');
            if (progressBars.length > 0) {
                progressBars.forEach(bar => {
                    const target = parseFloat(bar.getAttribute('aria-valuenow'));
                    
                    // Start from 0 and animate to the target value
                    let width = 0;
                    bar.style.width = '0%';
                    
                    const interval = setInterval(() => {
                        if (width >= target) {
                            clearInterval(interval);
                        } else {
                            width += 2;
                            bar.style.width = width + '%';
                            bar.textContent = Math.round(width) + '%';
                        }
                    }, 20);
                });
            }
        });
    </script>
</body>
</html>
"""

INDEX_TEMPLATE = """
{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h1 class="h3 mb-0 text-center">Detect Fake News</h1>
            </div>
            <div class="card-body">
                <p class="lead text-center mb-4">
                    Enter a news article or social media post to analyze its credibility.
                </p>
                
                <form action="/analyze" method="POST" id="analysis-form">
                    <div class="mb-3">
                        <label for="title" class="form-label">Article Title <small class="text-muted">(Optional)</small></label>
                        <input type="text" class="form-control" id="title" name="title" placeholder="Enter article title">
                    </div>
                    
                    <div class="mb-3">
                        <label for="content" class="form-label">Content <span class="text-danger">*</span></label>
                        <textarea class="form-control" id="content" name="content" rows="8" placeholder="Paste the article text or social media post content here" required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="source" class="form-label">Source <small class="text-muted">(Optional)</small></label>
                                <input type="text" class="form-control" id="source" name="source" placeholder="e.g., CNN, Twitter, Facebook">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="author" class="form-label">Author <small class="text-muted">(Optional)</small></label>
                                <input type="text" class="form-control" id="author" name="author" placeholder="Author's name">
                            </div>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-search me-2"></i>Analyze
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <div class="card shadow mt-4">
            <div class="card-header bg-info text-white">
                <h2 class="h4 mb-0">How It Works</h2>
            </div>
            <div class="card-body">
                <div class="row text-center">
                    <div class="col-md-4 mb-3 mb-md-0">
                        <div class="p-3">
                            <i class="fas fa-file-alt fa-3x text-primary mb-3"></i>
                            <h3 class="h5">Input Content</h3>
                            <p class="text-muted">Paste news article or social media content</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3 mb-md-0">
                        <div class="p-3">
                            <i class="fas fa-brain fa-3x text-primary mb-3"></i>
                            <h3 class="h5">AI Analysis</h3>
                            <p class="text-muted">Our model analyzes linguistic patterns and content</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="p-3">
                            <i class="fas fa-chart-pie fa-3x text-primary mb-3"></i>
                            <h3 class="h5">Get Results</h3>
                            <p class="text-muted">Receive credibility assessment with confidence score</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

RESULT_TEMPLATE = """
{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <!-- Result Summary Card -->
        <div class="card shadow mb-4 result-card">
            <div class="card-header {% if result.fake_probability > 0.7 %}bg-danger{% elif result.fake_probability > 0.4 %}bg-warning{% else %}bg-success{% endif %} text-white">
                <h2 class="h3 mb-0 text-center">Analysis Result</h2>
            </div>
            <div class="card-body">
                <div class="text-center mb-4">
                    <div class="display-1 mb-3">
                        {% if result.fake_probability > 0.7 %}
                            <i class="fas fa-exclamation-triangle text-danger"></i>
                        {% elif result.fake_probability > 0.4 %}
                            <i class="fas fa-question-circle text-warning"></i>
                        {% else %}
                            <i class="fas fa-check-circle text-success"></i>
                        {% endif %}
                    </div>
                    <h3 class="h2 mb-2 fw-bold {% if result.fake_probability > 0.7 %}text-danger{% elif result.fake_probability > 0.4 %}text-warning{% else %}text-success{% endif %}">
                        {{ result.result }}
                    </h3>
                    <p class="lead text-muted">
                        Confidence: <span class="fw-bold">{{ result.confidence }}</span>
                    </p>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-6 mb-3 mb-md-0">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <h4 class="h5 text-danger mb-3">Fake News Probability</h4>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-danger" role="progressbar" style="width: {{ result.fake_probability * 100 }}%" 
                                        aria-valuenow="{{ result.fake_probability * 100 }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ "%.1f"|format(result.fake_probability * 100) }}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <h4 class="h5 text-success mb-3">Real News Probability</h4>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" role="progressbar" style="width: {{ result.real_probability * 100 }}%" 
                                        aria-valuenow="{{ result.real_probability * 100 }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ "%.1f"|format(result.real_probability * 100) }}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Analyzed Content -->
                <div class="mb-4">
                    <h4 class="mb-3">Analyzed Content</h4>
                    {% if title %}
                        <h5 class="fw-bold">{{ title }}</h5>
                    {% endif %}
                    {% if source %}
                        <p class="text-muted mb-2">Source: {{ source }}</p>
                    {% endif %}
                    <div class="content-box">
                        {{ content }}
                    </div>
                </div>
                
                <!-- Recommendations -->
                <div class="card mb-3">
                    <div class="card-header bg-info text-white">
                        <h4 class="h5 mb-0">Recommendations</h4>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            {% if result.fake_probability > 0.5 %}
                                <li class="list-group-item">Verify this information with reputable sources</li>
                                <li class="list-group-item">Be cautious about sharing this content</li>
                                <li class="list-group-item">Check the original source for credibility</li>
                            {% else %}
                                <li class="list-group-item">Content appears credible, but always maintain healthy skepticism</li>
                                <li class="list-group-item">Cross-reference with other reputable sources when possible</li>
                            {% endif %}
                            <li class="list-group-item">Remember that our AI models have limitations and may not be 100% accurate</li>
                        </ul>
                    </div>
                </div>
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-center mt-4">
                    <a href="/" class="btn btn-primary">
                        <i class="fas fa-search me-2"></i>Analyze Another Article
                    </a>
                    <a href="/about" class="btn btn-outline-secondary">
                        <i class="fas fa-info-circle me-2"></i>Learn More
                    </a>
                </div>
            </div>
            <div class="card-footer text-muted text-center">
                Analysis performed on {{ result.timestamp }}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

ABOUT_TEMPLATE = """
{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h1 class="h3 mb-0">About the Fake News Detection System</h1>
            </div>
            <div class="card-body">
                <div class="mb-4">
                    <h2 class="h4 border-bottom pb-2">Project Overview</h2>
                    <p>The Fake News Detection System is an AI-powered tool designed to help identify potentially misleading information in news articles and social media content. In today's digital age, misinformation spreads rapidly across social networks, making automated detection tools increasingly important.</p>
                    <p>This project combines natural language processing, machine learning, and content analysis to evaluate the credibility of content based on various linguistic and contextual features.</p>
                </div>
                
                <div class="mb-4">
                    <h2 class="h4 border-bottom pb-2">How It Works</h2>
                    <div class="row text-center mb-4">
                        <div class="col-md-3 mb-3 mb-md-0">
                            <div class="p-3">
                                <i class="fas fa-file-alt fa-2x text-primary mb-3"></i>
                                <h3 class="h5">Input Collection</h3>
                                <p class="small text-muted">User enters content</p>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3 mb-md-0">
                            <div class="p-3">
                                <i class="fas fa-code fa-2x text-primary mb-3"></i>
                                <h3 class="h5">Analysis</h3>
                                <p class="small text-muted">Text pattern evaluation</p>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3 mb-md-0">
                            <div class="p-3">
                                <i class="fas fa-brain fa-2x text-primary mb-3"></i>
                                <h3 class="h5">Assessment</h3>
                                <p class="small text-muted">Credibility scoring</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="p-3">
                                <i class="fas fa-chart-pie fa-2x text-primary mb-3"></i>
                                <h3 class="h5">Results</h3>
                                <p class="small text-muted">Probability output</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mb-4">
                    <h2 class="h4 border-bottom pb-2">Limitations</h2>
                    <p>While our system employs pattern recognition techniques to detect fake news, it has several limitations:</p>
                    <ul>
                        <li>No detection system is 100% accurate; our tool provides probabilities, not certainties</li>
                        <li>This simplified version uses basic keyword and pattern analysis</li>
                        <li>Context and cultural nuances can sometimes lead to misclassification</li>
                        <li>For critical decisions, always cross-verify with multiple trusted sources</li>
                    </ul>
                </div>
                
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading"><i class="fas fa-info-circle me-2"></i>Responsible Use</h4>
                    <p>This tool is meant to assist users in evaluating content credibility but should not be the sole determinant. Critical thinking and verification with trusted sources remain essential.</p>
                    <hr>
                    <p class="mb-0">Remember that detecting fake news is an evolving challenge, and no single tool can replace media literacy and critical thinking skills.</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# Register templates
@app.template_filter('format')
def format_filter(value, format_spec):
    return format(value, format_spec)

app.jinja_env.globals.update({
    'extends': lambda template_name: f'{{% extends "{template_name}" %}}',
    'block': lambda block_name: f'{{% block {block_name} %}}',
    'endblock': lambda: f'{{% endblock %}}'
})

# Register the base template
@app.route('/base.html')
def base_template():
    return BASE_TEMPLATE

# Define routes
@app.route('/')
def index():
    """Render the home page."""
    return render_template_string(INDEX_TEMPLATE, base=BASE_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze submitted text."""
    if request.method == 'POST':
        # Get form data
        content = request.form.get('content', '')
        title = request.form.get('title', '')
        source = request.form.get('source', '')
        author = request.form.get('author', '')
        
        # Simple keyword-based analysis
        fake_keywords = [
            'conspiracy', 'shocking', 'they don\'t want you to know', 
            'secret', 'cover-up', 'hoax', 'scam', 'miracle', 'cure',
            'controversial', 'anonymous', 'whistleblower', 'hidden',
            'government', 'exposed', 'shocking truth', 'censored',
            'what they don\'t tell you', 'suppressed', 'banned'
        ]
        
        # Credibility indicators
        credibility_indicators = [
            'research shows', 'study finds', 'according to', 'evidence suggests',
            'experts say', 'data indicates', 'verified', 'confirmed by',
            'official', 'peer-reviewed', 'published in', 'sources confirmed'
        ]
        
        # Count fake news keywords
        content_lower = content.lower() + " " + title.lower()
        keyword_count = sum(1 for keyword in fake_keywords if keyword.lower() in content_lower)
        
        # Count credibility indicators
        credibility_count = sum(1 for indicator in credibility_indicators if indicator.lower() in content_lower)
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
        excessive_caps = caps_ratio > 0.2
        
        # Check for excessive punctuation
        exclamation_count = content.count('!')
        question_count = content.count('?')
        excessive_punctuation = (exclamation_count + question_count) > len(content.split()) / 10
        
        # Check for numbers and statistics without sources
        numbers_pattern = r'\d+%|\d+ percent|\d+ times'
        numbers_without_sources = len(re.findall(numbers_pattern, content_lower)) > 0 and credibility_count == 0
        
        # Initial score based on keyword count
        base_score = min(0.9, keyword_count * 0.15)  # Cap at 0.9
        
        # Adjust based on text length (short texts with keywords are more suspicious)
        if len(content.split()) < 50 and keyword_count > 0:
            base_score = max(base_score, 0.6)
            
        # Adjust based on other factors
        if excessive_caps:
            base_score += 0.1
        if excessive_punctuation:
            base_score += 0.1
        if numbers_without_sources:
            base_score += 0.1
            
        # Reduce score based on credibility indicators
        base_score = max(0.1, base_score - (credibility_count * 0.07))
        
        # Source credibility adjustment
        if source:
            source_lower = source.lower()
            credible_sources = ['bbc', 'reuters', 'associated press', 'ap', 'npr', 'washington post', 
                              'new york times', 'cnn', 'scientific american', 'nature', 'science']
            uncredible_sources = ['gossip', 'rumor', 'tabloid', 'conspiracy', 'truth', 'exposing']
            
            if any(s in source_lower for s in credible_sources):
                base_score = max(0.1, base_score - 0.2)
            elif any(s in source_lower for s in uncredible_sources):
                base_score = min(0.9, base_score + 0.2)
        
        # Add some randomness for demonstration (but keep within reasonable bounds)
        fake_prob = min(0.95, max(0.05, base_score + (random.random() - 0.5) * 0.1))
        
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
        
        # Prepare result data
        from datetime import datetime
        result_data = {
            "result": result,
            "confidence": confidence,
            "fake_probability": fake_prob,
            "real_probability": 1 - fake_prob,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Render the result page
        return render_template_string(RESULT_TEMPLATE, 
                                     content=content,
                                     title=title,
                                     source=source,
                                     result=result_data,
                                     base=BASE_TEMPLATE)

@app.route('/about')
def about():
    """Render the about page."""
    return render_template_string(ABOUT_TEMPLATE, base=BASE_TEMPLATE)

if __name__ == '__main__':
    # Print information
    print("=" * 80)
    print("Fake News Detection System - Simplified Version")
    print("=" * 80)
    print("Starting web application...")
    print("Once started, you can access the application at http://localhost:8080")
    print("Press Ctrl+C to stop the application")
    print("=" * 80)
    
    # Run the app
    app.run(host='0.0.0.0', port=8080, debug=True)
