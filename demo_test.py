#!/usr/bin/env python3
"""
Demo script to test TruthLens AI functionality
"""

import requests
import json
import base64

BASE_URL = "http://localhost:5001"

def test_analysis(text, language="en"):
    """Test the analysis endpoint"""
    print(f"\n🔍 Testing analysis in {language}...")
    print(f"Text: {text}")
    
    data = {
        'text': text,
        'language': language
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/analyze", data=data)
        result = response.json()
        
        if result.get('success'):
            analysis = result['data']
            print(f"✅ Result: {'REAL' if analysis['isReal'] else 'FAKE'}")
            print(f"📊 Confidence: {analysis['confidence']}%")
            print(f"🧠 Reasoning: {analysis['reasoning']}")
            return analysis
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_tts(text, language="en"):
    """Test the text-to-speech endpoint"""
    print(f"\n🔊 Testing TTS in {language}...")
    
    data = {
        'text': text,
        'language': language
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/text-to-speech",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        result = response.json()
        
        if result.get('success'):
            print("✅ TTS audio generated successfully!")
            audio_data = result['audio']
            print(f"📊 Audio data length: {len(audio_data)} characters")
            return True
        else:
            print(f"❌ TTS Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ TTS Request failed: {e}")
        return False

def main():
    print("🚀 TruthLens AI Demo Test")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "text": "Breaking: NASA confirms Earth will experience darkness for 15 days!",
            "language": "en",
            "expected": "FAKE"
        },
        {
            "text": "According to a peer-reviewed study published in Nature, scientists report new climate findings.",
            "language": "en",
            "expected": "REAL"
        },
        {
            "text": "¡Increíble! Los científicos descubren que beber agua fría causa cáncer.",
            "language": "es",
            "expected": "FAKE"
        },
        {
            "text": "Selon une étude publiée dans Nature, les chercheurs rapportent de nouvelles découvertes.",
            "language": "fr",
            "expected": "REAL"
        }
    ]
    
    # Run analysis tests
    print("\n📝 ANALYSIS TESTS:")
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        result = test_analysis(case["text"], case["language"])
        
        if result:
            actual = "REAL" if result['isReal'] else "FAKE"
            status = "✅ PASS" if actual == case["expected"] else "⚠️  UNEXPECTED"
            print(f"Expected: {case['expected']}, Got: {actual} {status}")
    
    # Test TTS
    print("\n🔊 TEXT-TO-SPEECH TESTS:")
    tts_tests = [
        ("This news appears to be fake.", "en"),
        ("Esta noticia parece ser falsa.", "es"),
        ("Cette nouvelle semble être fausse.", "fr")
    ]
    
    for text, lang in tts_tests:
        test_tts(text, lang)
    
    print("\n✨ Demo test completed!")
    print(f"🌐 Visit {BASE_URL} to test the web interface")

if __name__ == "__main__":
    main()
