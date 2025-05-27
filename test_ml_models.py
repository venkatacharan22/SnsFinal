#!/usr/bin/env python3
"""
Test script for ML models and new functionality
"""

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def preprocess_text(text):
    """Clean and preprocess text for model prediction"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def test_ml_models():
    """Test if ML models can be loaded and used"""
    print("🧪 Testing ML Models...")
    
    try:
        # Load models
        print("📦 Loading models...")
        with open('fake_news_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        
        print("✅ Models loaded successfully!")
        print(f"📊 Model type: {type(model)}")
        print(f"📊 Vectorizer type: {type(vectorizer)}")
        
        # Test predictions
        test_texts = [
            "Breaking: Scientists discover cure for all diseases!",
            "NASA confirms Earth will experience darkness for 15 days due to planetary alignment!",
            "Local weather forecast shows rain expected tomorrow.",
            "President announces new economic policy in official statement.",
            "SHOCKING: Doctors hate this one weird trick that cures everything!"
        ]
        
        print("\n🔍 Testing predictions:")
        print("-" * 60)
        
        for i, text in enumerate(test_texts, 1):
            # Preprocess
            cleaned_text = preprocess_text(text)
            
            # Vectorize
            text_vectorized = vectorizer.transform([cleaned_text])
            
            # Predict
            prediction = model.predict(text_vectorized)[0]
            prediction_proba = model.predict_proba(text_vectorized)[0]
            confidence = max(prediction_proba)
            
            is_fake = bool(prediction)
            status = "FAKE" if is_fake else "REAL"
            
            print(f"{i}. Text: {text[:50]}...")
            print(f"   Prediction: {status} ({confidence:.2%} confidence)")
            print(f"   Probabilities: {prediction_proba}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔧 Testing Dependencies...")
    
    dependencies = [
        ('numpy', 'np'),
        ('pandas', 'pd'),
        ('sklearn', 'sklearn'),
        ('PIL', 'PIL'),
        ('cv2', 'cv2'),
        ('pytesseract', 'pytesseract'),
        ('gtts', 'gtts'),
        ('google.generativeai', 'genai')
    ]
    
    missing = []
    
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {dep_name}")
        except ImportError:
            print(f"❌ {dep_name} - MISSING")
            missing.append(dep_name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    else:
        print("\n✅ All dependencies available!")
        return True

def main():
    """Main test function"""
    print("🚀 TruthLens AI - ML Model Testing")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    print()
    
    # Test ML models
    models_ok = test_ml_models()
    print()
    
    # Summary
    print("📋 Test Summary:")
    print(f"   Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"   ML Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    
    if deps_ok and models_ok:
        print("\n🎉 All tests passed! Ready for deployment.")
        print("\n🚀 To run the application:")
        print("   python3 app.py")
        print("\n🌐 Then visit: http://localhost:5001")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
