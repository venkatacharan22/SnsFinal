from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import base64
from PIL import Image
import io
import pyttsx3
import threading
from gtts import gTTS
import tempfile

app = Flask(__name__)
CORS(app)

# Configure Gemini API (using Gemini as Gemma 3 27B isn't directly available via API)
genai.configure(api_key="AIzaSyCBv8jNE-5K8Ojs0UumdeBL_Zba68b4e18")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

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
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        text = request.form.get('text', '')
        image_file = request.files.get('image')
        language = request.form.get('language', 'en')

        if not text and not image_file:
            return jsonify({'error': 'Either text or image must be provided'}), 400

        # Prepare content for Gemini
        content = []

        # Add text if provided
        if text:
            content.append(create_prompt(text, bool(image_file), language))

        # Add image if provided
        if image_file:
            image = Image.open(image_file.stream)
            content.append(image)
            if not text:
                content.append(create_prompt("", True, language))

        # Generate response
        response = model.generate_content(
            content,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )
        )

        # Parse JSON response
        result_text = response.text.strip()
        # Clean up response
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]

        result = json.loads(result_text)

        return jsonify({
            'success': True,
            'data': result
        })

    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': 'Failed to parse AI response'
        }), 500
    except Exception as e:
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

        # Create TTS audio
        tts = gTTS(text=text, lang=language, slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)

            # Read the file and encode as base64
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

        # Clean up temp file
        os.unlink(tmp_file.name)

        return jsonify({
            'success': True,
            'audio': audio_data,
            'format': 'mp3'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
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
    app.run(debug=True, host='0.0.0.0', port=5001)
