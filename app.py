from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import base64
from PIL import Image
import io
import pickle
import numpy as np
import pandas as pd
from gtts import gTTS
import tempfile
import os
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pytesseract
import cv2

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5001",
    "http://localhost:5002",
    "https://sns01-a8fba.web.app",
    "https://sns01-a8fba.firebaseapp.com",
    "https://storage.googleapis.com"
])

# Configure Gemini API for explanations
genai.configure(api_key="AIzaSyCBv8jNE-5K8Ojs0UumdeBL_Zba68b4e18")
gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Load trained models
print("Loading ML models...")
try:
    with open('fake_news_model.pkl', 'rb') as f:
        fake_news_model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    print("✅ ML models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    fake_news_model = None
    tfidf_vectorizer = None

# Language mappings
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'sv': 'Swedish'
}

# Text preprocessing function
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

# OCR function for image text extraction
def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        # Convert PIL image to numpy array for OpenCV
        img_array = np.array(image)

        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(img_array)

        return extracted_text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

# ML Model prediction function
def predict_fake_news(text):
    """Predict if news is fake using trained ML model"""
    try:
        if not fake_news_model or not tfidf_vectorizer:
            return None, 0.5

        # Preprocess text
        cleaned_text = preprocess_text(text)

        if not cleaned_text:
            return None, 0.5

        # Vectorize text using trained TF-IDF vectorizer
        text_vectorized = tfidf_vectorizer.transform([cleaned_text])

        # Get prediction and probability
        prediction = fake_news_model.predict(text_vectorized)[0]
        prediction_proba = fake_news_model.predict_proba(text_vectorized)[0]

        # Get confidence (probability of the predicted class)
        confidence = max(prediction_proba)

        # Convert prediction to boolean
        # Based on testing: 0 = fake, 1 = real (inverted from standard)
        is_fake = not bool(prediction)  # Invert the prediction

        return is_fake, confidence

    except Exception as e:
        print(f"ML Prediction Error: {e}")
        return None, 0.5

# Gemini explanation function
def get_gemini_explanation(text, is_fake, confidence, language='en'):
    """Get explanation from Gemini AI about why news is fake/real in the specified language"""
    try:
        # Enhanced language mapping with native names
        language_names = {
            'hi': 'Hindi (हिंदी)',
            'ta': 'Tamil (தமிழ்)',
            'te': 'Telugu (తెలుగు)',
            'ml': 'Malayalam (മലയാളം)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'bn': 'Bengali (বাংলা)',
            'gu': 'Gujarati (ગુજરાતી)',
            'mr': 'Marathi (मराठी)',
            'pa': 'Punjabi (ਪੰਜਾਬੀ)',
            'en': 'English',
            'es': 'Spanish (Español)',
            'fr': 'French (Français)',
            'de': 'German (Deutsch)',
            'it': 'Italian (Italiano)',
            'pt': 'Portuguese (Português)',
            'ru': 'Russian (Русский)',
            'ja': 'Japanese (日本語)',
            'ko': 'Korean (한국어)',
            'zh': 'Chinese (中文)',
            'ar': 'Arabic (العربية)',
            'tr': 'Turkish (Türkçe)',
            'nl': 'Dutch (Nederlands)',
            'sv': 'Swedish (Svenska)'
        }

        status = "FAKE" if is_fake else "REAL"
        language_name = language_names.get(language, 'English')

        prompt = f"""
        You are an expert multilingual fact-checker. A machine learning model has analyzed news content and classified it as {status} with {confidence:.1%} confidence.

        News Text: "{text}"

        CRITICAL: Respond ENTIRELY in {language_name}. Use native script where applicable (Devanagari for Hindi, Tamil script for Tamil, etc.).

        Provide a comprehensive explanation covering:

        1. **ML Analysis**: Why the model classified this as {status.lower()}
        2. **Key Indicators**: Specific patterns that led to this classification
        3. **Verification Tips**: How readers can fact-check such content
        4. **Cultural Context**: Misinformation patterns relevant to {language_name} speakers
        5. **Action Steps**: What readers should do next

        Requirements:
        - Write ONLY in {language_name}
        - Use appropriate cultural context
        - Be educational and helpful
        - Explain in simple, clear terms
        - Provide practical advice

        Format as a flowing, educational explanation that empowers users to be better news consumers.
        """

        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,  # Lower for more consistent multilingual output
                max_output_tokens=1500  # More tokens for detailed explanations
            )
        )

        return response.text

    except Exception as e:
        print(f"Gemini Explanation Error: {e}")
        # Provide fallback explanations in the target language
        fallback_explanations = {
            'hi': f"मशीन लर्निंग मॉडल ने इस समाचार को {confidence:.1%} विश्वास के साथ {status} के रूप में वर्गीकृत किया है। कृपया कई विश्वसनीय स्रोतों से सत्यापन करें।",
            'ta': f"இயந்திர கற்றல் மாதிரி இந்த செய்தியை {confidence:.1%} நம்பிக்கையுடன் {status} என வகைப்படுத்தியுள்ளது। பல நம்பகமான ஆதாரங்களில் இருந்து சரிபார்க்கவும்।",
            'te': f"మెషిన్ లెర్నింగ్ మోడల్ ఈ వార్తను {confidence:.1%} విశ్వాసంతో {status} గా వర్గీకరించింది। దయచేసి అనేక విశ్వసనీయ మూలాల నుండి ధృవీకరించండి।",
            'ml': f"മെഷീൻ ലേണിംഗ് മോഡൽ ഈ വാർത്തയെ {confidence:.1%} വിശ്വാസത്തോടെ {status} ആയി തരംതിരിച്ചിട്ടുണ്ട്. ദയവായി ഒന്നിലധികം വിശ്വസനീയ സ്രോതസ്സുകളിൽ നിന്ന് പരിശോധിക്കുക।",
            'kn': f"ಯಂತ್ರ ಕಲಿಕೆ ಮಾದರಿಯು ಈ ಸುದ್ದಿಯನ್ನು {confidence:.1%} ವಿಶ್ವಾಸದೊಂದಿಗೆ {status} ಎಂದು ವರ್ಗೀಕರಿಸಿದೆ. ದಯವಿಟ್ಟು ಅನೇಕ ವಿಶ್ವಾಸಾರ್ಹ ಮೂಲಗಳಿಂದ ಪರಿಶೀಲಿಸಿ।",
            'en': f"The machine learning model classified this news as {status} with {confidence:.1%} confidence. Please verify through multiple reliable sources."
        }
        return fallback_explanations.get(language, fallback_explanations['en'])

def create_prompt(text, has_image=False, language='en'):
    language_name = LANGUAGES.get(language, 'English')

    return f"""You are a multilingual fact-checking expert AI trained to detect misinformation and verify news claims across different languages and cultures.

IMPORTANT: Respond in {language_name} language. All text fields in the JSON response must be in {language_name}.

{'MULTIMODAL ANALYSIS: Examine both the text content and any visual elements in the image for authenticity, manipulation, misleading context, or out-of-context usage.' if has_image else ''}

Given the news statement below, do the following:
1. Use your internal knowledge and reasoning to determine if the claim is TRUE or FALSE
2. Cross-check it with scientific consensus, verified public statements, and established facts
3. Check if this claim has been previously debunked by fact-checkers globally
4. Analyze language patterns for sensationalism or manipulation tactics
5. Consider cultural context and regional misinformation patterns

REQUIRED JSON RESPONSE FORMAT (all text in {language_name}):
{{
  "isReal": boolean,
  "confidence": number (70-95),
  "reasoning": "Detailed explanation in {language_name} based on factual evidence, scientific consensus, or lack thereof. If previously debunked, mention that clearly (2-3 sentences)",
  "sources": [
    {{"name": "Credible Source Name in {language_name}", "credibility": "High|Medium|Low"}}
  ],
  "redFlags": ["specific warning signs in {language_name}"],
  "factualClaims": ["verifiable claims in {language_name}"],
  "recommendation": "Clear actionable advice for readers in {language_name}",
  "debunkedBy": ["fact-checking organizations if applicable"],
  "language": "{language}",
  "summary": "Brief one-sentence summary in {language_name}"
}}

FACT-CHECKING CRITERIA:
🟢 REAL NEWS INDICATORS:
- Verifiable through multiple credible sources
- Consistent with scientific consensus
- Reported by established news organizations
- Contains specific, checkable details
- No history of being debunked

🔴 FAKE NEWS INDICATORS:
- Contradicts established scientific facts
- Uses sensational or fear-inducing language
- Lacks credible source attribution
- Has been debunked by fact-checkers
- Contains impossible or implausible claims
- Designed to provoke emotional reactions

CONFIDENCE LEVELS:
- 90-95%: Definitive evidence (scientifically proven/debunked)
- 80-89%: Strong evidence from multiple credible sources
- 70-79%: Moderate confidence with some uncertainty

{'IMAGE VERIFICATION: Check for signs of digital manipulation, misleading captions, reverse image search indicators, or images taken out of context.' if has_image else ''}

News to analyze: "{text or 'Analyze the uploaded image content'}"

Remember: Provide ONLY the JSON response with all text fields in {language_name}, no additional text."""

@app.route('/')
def index():
    # Add cache busting to force browser refresh
    import time
    cache_buster = str(int(time.time()))
    return render_template('index.html', cache_buster=cache_buster)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        text = request.form.get('text', '')
        image_file = request.files.get('image')
        language = request.form.get('language', 'en')

        if not text and not image_file:
            return jsonify({'error': 'Either text or image must be provided'}), 400

        # Extract text from image if provided
        extracted_text = ""
        if image_file:
            try:
                image = Image.open(image_file.stream)
                extracted_text = extract_text_from_image(image)
                print(f"Extracted text from image: {extracted_text[:100]}...")
            except Exception as e:
                print(f"Image processing error: {e}")

        # Combine text sources
        analysis_text = text
        if extracted_text:
            analysis_text = f"{text} {extracted_text}".strip()

        if not analysis_text:
            return jsonify({'error': 'No text found to analyze'}), 400

        print(f"Analyzing text: {analysis_text[:100]}...")

        # Step 1: Use ML model for prediction
        is_fake, ml_confidence = predict_fake_news(analysis_text)

        if is_fake is None:
            return jsonify({
                'success': False,
                'error': 'ML model prediction failed'
            }), 500

        # Step 2: Get Gemini explanation
        explanation = get_gemini_explanation(analysis_text, is_fake, ml_confidence, language)

        # Step 3: Create response in the expected format
        confidence_percentage = int(ml_confidence * 100)

        # Generate sources based on prediction
        sources = [
            {"name": "ML Model Analysis", "credibility": "High"},
            {"name": "TF-IDF Vectorization", "credibility": "High"}
        ]

        # Generate red flags for fake news
        red_flags = []
        if is_fake:
            red_flags = [
                "Suspicious language patterns detected",
                "Content characteristics match fake news training data",
                "High probability of misinformation"
            ]

        # Create result
        result = {
            "isReal": not is_fake,
            "confidence": confidence_percentage,
            "reasoning": explanation,
            "sources": sources,
            "redFlags": red_flags,
            "factualClaims": [analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text],
            "recommendation": "Always verify news through multiple reliable sources before sharing." if is_fake else "Content appears credible, but always cross-check with multiple sources.",
            "debunkedBy": ["ML Model Classification"] if is_fake else [],
            "language": language,
            "summary": f"ML Model classified as {'FAKE' if is_fake else 'REAL'} with {confidence_percentage}% confidence",
            "mlPrediction": {
                "isFake": is_fake,
                "confidence": ml_confidence,
                "model": "Trained Kaggle Model"
            }
        }

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Language mapping for gTTS (some languages need specific codes)
        tts_lang_map = {
            'hi': 'hi',    # Hindi
            'ta': 'ta',    # Tamil
            'te': 'te',    # Telugu
            'ml': 'ml',    # Malayalam
            'kn': 'kn',    # Kannada
            'bn': 'bn',    # Bengali
            'gu': 'gu',    # Gujarati
            'mr': 'mr',    # Marathi
            'pa': 'pa',    # Punjabi
            'en': 'en',    # English
            'es': 'es',    # Spanish
            'fr': 'fr',    # French
            'de': 'de',    # German
            'it': 'it',    # Italian
            'pt': 'pt',    # Portuguese
            'ru': 'ru',    # Russian
            'ja': 'ja',    # Japanese
            'ko': 'ko',    # Korean
            'zh': 'zh-cn', # Chinese (Simplified)
            'ar': 'ar',    # Arabic
            'tr': 'tr',    # Turkish
            'nl': 'nl',    # Dutch
            'sv': 'sv'     # Swedish
        }

        # Get the correct TTS language code
        tts_language = tts_lang_map.get(language, 'en')

        print(f"TTS Request - Text: {text[:50]}..., Language: {language} -> {tts_language}")

        # Create TTS audio with error handling
        try:
            print(f"Creating TTS with language: {tts_language}")
            tts = gTTS(text=text, lang=tts_language, slow=False)
            print("TTS object created successfully")
        except Exception as tts_error:
            print(f"TTS Error for language {tts_language}: {tts_error}")
            # Fallback to English if the language is not supported
            print("Falling back to English...")
            tts_language = 'en'
            tts = gTTS(text=text, lang='en', slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            print(f"Saving TTS to temporary file: {tmp_file.name}")
            tts.save(tmp_file.name)
            print("TTS saved successfully")

            # Read the file and encode as base64
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
                print(f"Audio data encoded, size: {len(audio_data)} characters")

        # Clean up temp file
        try:
            os.unlink(tmp_file.name)
            print("Temporary file cleaned up")
        except Exception as cleanup_error:
            print(f"Warning: Could not clean up temp file: {cleanup_error}")

        return jsonify({
            'success': True,
            'audio': audio_data,
            'format': 'mp3',
            'language': tts_language
        })

    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Text-to-speech failed: {str(e)}'
        }), 500

@app.route('/api/languages')
def get_languages():
    return jsonify({
        'success': True,
        'languages': LANGUAGES
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'OK', 'service': 'TruthLens AI'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
