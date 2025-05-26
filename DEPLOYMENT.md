# 🚀 TruthLens AI Firebase Deployment Guide

## 📋 Prerequisites

1. **Firebase Project**: You mentioned you already have one created ✅
2. **Firebase CLI**: Installed ✅
3. **Google Account**: With access to your Firebase project ✅

## 🔧 Step-by-Step Deployment

### Step 1: Login to Firebase

```bash
firebase login
```

### Step 2: Set Your Project ID

1. **Find your project ID** from Firebase Console
2. **Update `.firebaserc`** file:
   ```json
   {
     "projects": {
       "default": "your-actual-project-id"
     }
   }
   ```

### Step 3: Initialize Firebase (if needed)

```bash
firebase use your-project-id
```

### Step 4: Deploy to Firebase Hosting

```bash
firebase deploy
```

## 🌐 What Gets Deployed

### Frontend (Firebase Hosting)
- ✅ **Static Website**: Complete responsive UI
- ✅ **23 Languages**: All language support
- ✅ **Mobile Optimized**: Touch-friendly interface
- ✅ **Cyber Theme**: Neon animations and effects

### Backend Options

Since Firebase Hosting only serves static files, you have several options for the backend:

#### Option 1: Google Cloud Functions (Recommended)
```bash
# Install Firebase Functions
npm install -g firebase-functions

# Initialize functions
firebase init functions

# Deploy functions
firebase deploy --only functions
```

#### Option 2: Google Cloud Run
- Deploy the Flask app as a container
- More suitable for complex Python applications

#### Option 3: External Hosting
- Deploy backend to Heroku, Railway, or DigitalOcean
- Update the `API_BASE_URL` in the frontend

## 🔄 Current Setup

The frontend is configured to:
- Use `localhost:5001` for local development
- Use `https://your-backend-url.com` for production

**You need to update this URL** in `public/index.html`:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5001' 
    : 'https://your-actual-backend-url.com'; // Update this!
```

## 📱 After Deployment

Your website will be available at:
- `https://your-project-id.web.app`
- `https://your-project-id.firebaseapp.com`

## 🔧 Backend Deployment Options

### Option A: Convert to Firebase Functions

Create `functions/index.js`:
```javascript
const functions = require('firebase-functions');
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

// Your API routes here
app.post('/api/analyze', (req, res) => {
  // Implement Gemini API calls
});

exports.api = functions.https.onRequest(app);
```

### Option B: Deploy Flask to Cloud Run

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy truthlens-api --source .
```

### Option C: Use Heroku (Easiest)

1. Create `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 🧪 Testing Deployment

1. **Local Testing**:
   ```bash
   firebase serve
   ```

2. **Production Testing**:
   - Visit your Firebase URL
   - Test with sample news content
   - Verify all 23 languages work
   - Test mobile responsiveness

## 🔐 Environment Variables

For production, you'll need to:
1. **Secure your Gemini API key**
2. **Set up environment variables**
3. **Configure CORS properly**

## 📊 Monitoring

After deployment:
- Monitor Firebase Hosting analytics
- Check API usage in Google Cloud Console
- Monitor performance and errors

## 🆘 Troubleshooting

### Common Issues:
1. **CORS Errors**: Update backend CORS settings
2. **API Key Issues**: Check environment variables
3. **Build Errors**: Verify all files are included

### Quick Fixes:
```bash
# Redeploy
firebase deploy

# Check logs
firebase functions:log

# Test locally
firebase serve
```

## 📞 Support

If you encounter issues:
1. Check Firebase Console for errors
2. Review deployment logs
3. Test API endpoints individually
4. Verify project permissions

---

**Ready to deploy? Run `./deploy.sh` to start!** 🚀
