# 🔍 TruthLens AI - ML-Powered Fake News Detection

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![ML](https://img.shields.io/badge/ML-Kaggle%20Trained-green.svg)](https://kaggle.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)](https://ai.google.dev)
[![Mobile](https://img.shields.io/badge/Mobile-Responsive-purple.svg)](https://tailwindcss.com)

Advanced multilingual fake news detection system using **Kaggle-trained ML models** for prediction and **Gemini AI** for explanations, with OCR support and 23 languages.

## 🌟 Features

### 🤖 **ML-Powered Prediction**
- **Kaggle-Trained Models**: Real machine learning models for fake news detection
- **TF-IDF Vectorization**: Advanced text feature extraction
- **High Accuracy**: Trained on large datasets for reliable predictions
- **Confidence Scoring**: Probability-based confidence levels
- **Binary Classification**: Clear FAKE/REAL predictions

### 🧠 **AI Explanations**
- **Gemini 2.0 Flash**: Advanced AI for detailed explanations
- **Multilingual Explanations**: Responses in 23 languages
- **Educational Content**: Learn why content is classified as fake/real
- **Context Analysis**: Understanding of misinformation patterns

### 🇮🇳 **Indian Language Support**
- **10 Indian Languages**: Hindi, Tamil, Telugu, Malayalam, Kannada, Bengali, Gujarati, Marathi, Punjabi
- **Native Scripts**: Proper display of Devanagari, Tamil, Telugu, Malayalam scripts
- **Cultural Context**: AI understands regional misinformation patterns
- **OCR Support**: Extract text from images in Indian languages

### 📷 **Image Analysis with OCR**
- **Text Extraction**: Extract text from news screenshots and images
- **Tesseract OCR**: Multi-language optical character recognition
- **Image + Text Analysis**: Combine uploaded text with extracted text
- **Indian Language OCR**: Support for Hindi, Tamil, Telugu, and more

### 📱 **Mobile-First Design**
- **Fully Responsive**: Perfect on mobile, tablet, and desktop
- **Touch-Friendly**: Optimized for mobile interactions
- **Fast Loading**: Optimized performance for all devices
- **Cyber Theme**: Modern neon-styled interface

### 🔊 **Text-to-Speech**
- **Multi-language TTS**: Hear results in your selected language
- **Google TTS**: High-quality voice synthesis
- **Accessibility**: Audio support for visually impaired users

### 🖼️ **Image Analysis**
- **Upload Support**: Drag & drop image upload
- **Screenshot Analysis**: Analyze news screenshots
- **Visual Verification**: Detect manipulated images
- **Context Analysis**: Check for misleading captions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/venkatacharan22/SnsFinal.git
cd SnsFinal
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API key**
- Get your Gemini API key from [Google AI Studio](https://ai.google.dev)
- Update the API key in `app.py` (line 14)

4. **Run the application**
```bash
python3 app.py
```

5. **Open in browser**
```
http://localhost:5001
```

## 📖 Usage

### Web Interface
1. **Select Language**: Choose from 23 supported languages
2. **Enter Content**: Type news text or upload an image
3. **Analyze**: Click "Analyze for Truth" button
4. **View Results**: Get comprehensive analysis with confidence score
5. **Listen**: Use text-to-speech to hear results
6. **Share**: Copy results to clipboard

### API Endpoints

#### Analyze Content
```bash
POST /api/analyze
Content-Type: multipart/form-data

Parameters:
- text: News content to analyze
- image: Image file (optional)
- language: Output language code (default: 'en')
```

#### Text-to-Speech
```bash
POST /api/text-to-speech
Content-Type: application/json

Body:
{
  "text": "Text to convert to speech",
  "language": "en"
}
```

#### Get Languages
```bash
GET /api/languages
```

## 🌐 Supported Languages

### 🇮🇳 Indian Languages
| Code | Language | Script |
|------|----------|--------|
| `hi` | हिंदी (Hindi) | Devanagari |
| `ta` | தமிழ் (Tamil) | Tamil |
| `te` | తెలుగు (Telugu) | Telugu |
| `ml` | മലയാളം (Malayalam) | Malayalam |
| `kn` | ಕನ್ನಡ (Kannada) | Kannada |
| `bn` | বাংলা (Bengali) | Bengali |
| `gu` | ગુજરાતી (Gujarati) | Gujarati |
| `mr` | मराठी (Marathi) | Devanagari |
| `pa` | ਪੰਜਾਬੀ (Punjabi) | Gurmukhi |

### 🌍 International Languages
| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |
| `ja` | Japanese |
| `ko` | Korean |
| `zh` | Chinese |
| `ar` | Arabic |
| `tr` | Turkish |
| `nl` | Dutch |
| `sv` | Swedish |

## 🧪 Testing Examples

### Hindi (हिंदी)
```
तत्काल: नासा ने पुष्टि की है कि पृथ्वी पर 15 दिन तक अंधकार रहेगा ग्रहों की स्थिति के कारण!
```

### Tamil (தமிழ்)
```
அதிர்ச்சி: நாசா உறுதிப்படுத்தியுள்ளது - கிரக சீரமைப்பு காரணமாக பூமியில் 15 நாட்கள் இருள் நிலவும்!
```

### English
```
Breaking: NASA confirms Earth will experience darkness for 15 days due to planetary alignment!
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   Gemini AI     │
│                 │    │                 │    │                 │
│ • HTML5         │◄──►│ • Python Flask  │◄──►│ • Gemini 2.0    │
│ • Tailwind CSS  │    │ • Image Upload  │    │ • Flash Model   │
│ • JavaScript    │    │ • TTS Support   │    │ • Multilingual  │
│ • Responsive    │    │ • CORS Enabled  │    │ • Fact Checking │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Technical Details

### Backend
- **Framework**: Flask 3.0+
- **AI Model**: Google Gemini 2.0 Flash
- **TTS**: Google Text-to-Speech (gTTS)
- **Image Processing**: Pillow (PIL)
- **CORS**: Flask-CORS for cross-origin requests

### Frontend
- **Styling**: Tailwind CSS
- **JavaScript**: Vanilla ES6+
- **Design**: Mobile-first responsive
- **Theme**: Cyber neon with glassmorphism
- **Animations**: CSS keyframes and transitions

### Performance
- **Temperature**: 0.2 for factual responses
- **Max Tokens**: 2048 for detailed analysis
- **Caching**: Browser caching for static assets
- **Optimization**: Compressed images and minified CSS

## 📱 Mobile Features

- ✅ **Touch-Friendly**: Large buttons and touch targets
- ✅ **Responsive Grid**: Adapts to screen size
- ✅ **Readable Text**: Optimized font sizes
- ✅ **Fast Loading**: Optimized for mobile networks
- ✅ **Offline Ready**: Service worker support (coming soon)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini API
- **Tailwind CSS**: For the responsive design framework
- **Flask**: For the lightweight web framework
- **Contributors**: All developers who contributed to this project

## 📞 Support

For support, email [support@truthlens.ai](mailto:support@truthlens.ai) or create an issue on GitHub.

---

**Made with ❤️ for fighting misinformation in the digital age**
