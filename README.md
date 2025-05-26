# TruthLens AI - Fake News Detection System

A sophisticated web application that uses Google's Gemini AI to detect fake news and misinformation in both text and image content. Built with React, Node.js, and modern web technologies.

## 🌟 Features

### ✨ Core Functionality
- **Text Analysis**: Analyze news articles, headlines, and text content for authenticity
- **Image Analysis**: Upload and analyze news screenshots and images
- **AI-Powered Detection**: Powered by Google's Gemini 3 27B model via Vertex AI
- **Confidence Scoring**: Get percentage-based confidence scores (70-95%)
- **Source Credibility**: Analysis of potential sources and their credibility levels
- **Detailed Reasoning**: Comprehensive explanations for each analysis result

### 🎨 User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Glassmorphism UI**: Modern, elegant interface with glass-like effects
- **Dark/Light Mode**: Toggle between themes with smooth transitions
- **Smooth Animations**: Framer Motion powered animations throughout
- **Typewriter Effect**: Engaging hero section with animated text
- **Loading Animations**: Beautiful loading states during analysis

### 🔧 Technical Features
- **Real-time Analysis**: Fast processing with animated progress indicators
- **File Upload**: Drag-and-drop image upload with validation
- **Rate Limiting**: Built-in API rate limiting for stability
- **Error Handling**: Comprehensive error handling and user feedback
- **Demo Mode**: Fallback demo mode when API is not configured

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Google Cloud account (for production Gemini AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TruthLens-AI
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd ../backend
   npm install
   ```

4. **Configure Environment Variables**
   
   **Backend (.env):**
   ```env
   PORT=3001
   NODE_ENV=development
   GOOGLE_API_KEY=your-google-api-key
   GOOGLE_PROJECT_ID=your-project-id
   GOOGLE_LOCATION=us-central1
   FRONTEND_URL=http://localhost:5173
   ```

   **Frontend (.env):**
   ```env
   VITE_API_URL=http://localhost:3001
   ```

5. **Start the Development Servers**
   
   **Backend:**
   ```bash
   cd backend
   npm run dev
   ```

   **Frontend (in a new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3001
   - Health Check: http://localhost:3001/health

## 🏗️ Project Structure

```
TruthLens-AI/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   │   ├── Hero.jsx
│   │   │   ├── InputSection.jsx
│   │   │   ├── ResultSection.jsx
│   │   │   ├── LoadingAnimation.jsx
│   │   │   └── ThemeToggle.jsx
│   │   ├── hooks/          # Custom React hooks
│   │   │   └── useTheme.js
│   │   ├── utils/          # Utility functions
│   │   │   └── api.js
│   │   └── styles/         # CSS and styling
│   └── package.json
├── backend/                 # Node.js + Express backend
│   ├── routes/             # API routes
│   │   └── analyze.js
│   ├── services/           # Business logic
│   │   └── geminiService.js
│   ├── middleware/         # Express middleware
│   │   ├── upload.js
│   │   ├── validation.js
│   │   ├── errorHandler.js
│   │   └── rateLimiter.js
│   └── server.js
└── README.md
```

## 🔧 API Endpoints

### POST /api/analyze
Analyze text or image content for fake news detection.

**Request:**
```json
{
  "text": "News content to analyze"
}
```

Or with FormData for image upload:
```
text: "Optional text content"
image: [File object]
```

**Response:**
```json
{
  "success": true,
  "data": {
    "isReal": true,
    "confidence": 85,
    "reasoning": "Analysis explanation...",
    "sources": [
      {"name": "Reuters", "credibility": "High"}
    ],
    "redFlags": [],
    "factualClaims": ["Verifiable claims found"],
    "recommendation": "Verification recommendation"
  },
  "timestamp": "2025-05-26T03:28:01.900Z"
}
```

### GET /api/status
Check the status of the Gemini AI service.

### GET /health
Health check endpoint for the backend service.

## 🎯 Demo Mode

The application includes a demo mode that activates when:
- Running in development environment
- Google API key is not properly configured
- Gemini API is unavailable

Demo mode provides realistic simulated responses based on content analysis heuristics.

## 🔐 Google Cloud Setup

To use the real Gemini AI (production mode):

1. Create a Google Cloud Project
2. Enable the Vertex AI API
3. Create an API key or service account
4. Update the environment variables with your credentials

## 🛠️ Technologies Used

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Lucide React** - Icon library
- **Axios** - HTTP client

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Google Vertex AI** - AI/ML platform
- **Multer** - File upload handling
- **Helmet** - Security middleware
- **CORS** - Cross-origin resource sharing

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the demo mode functionality first
- Verify environment variables are set correctly
- Check browser console for any errors
- Ensure both frontend and backend servers are running

---

**Built with ❤️ using modern web technologies and AI**
