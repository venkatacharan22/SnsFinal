# 🚀 TruthLens AI - Google Cloud Complete Deployment

## 📋 Quick Start (5 Minutes)

### 1. Prerequisites Check
```bash
# Check if tools are installed
gcloud --version
firebase --version

# If not installed:
# gcloud: https://cloud.google.com/sdk/docs/install
# firebase: npm install -g firebase-tools
```

### 2. Set Project
```bash
# Set your Google Cloud project
gcloud config set project said-eb2f5

# Login to both services
gcloud auth login
firebase login
```

### 3. One-Click Deploy
```bash
cd /Users/asha/Semester\ 6/SNS-1
./deploy-gcp.sh
```

**That's it! Your app will be live in ~5 minutes.**

## 🎯 What Gets Deployed

### Backend (Cloud Run)
- **URL**: `https://truthlens-backend-XXXXX-uc.a.run.app`
- **Features**: ML models, Gemini AI, OCR, TTS
- **Specs**: 2GB RAM, 2 CPU cores, auto-scaling

### Frontend (Firebase Hosting)
- **URL**: `https://said-eb2f5.web.app`
- **Features**: Responsive UI, 23 languages, mobile-friendly
- **CDN**: Global content delivery network

## 🔧 Manual Deployment (If Needed)

### Step 1: Deploy Backend
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Deploy
gcloud builds submit --config cloudbuild.yaml

# Get URL
gcloud run services describe truthlens-backend --region=us-central1 --format="value(status.url)"
```

### Step 2: Update Frontend
```bash
# Update API URL in public/index.html (line 287)
# Replace: https://truthlens-backend-YOUR_PROJECT_ID-uc.a.run.app
# With: Your actual backend URL from Step 1
```

### Step 3: Deploy Frontend
```bash
firebase use said-eb2f5
firebase deploy --only hosting
```

## 🧪 Testing Your Deployment

### Test Backend
```bash
# Health check
curl https://your-backend-url/api/health

# Test analysis
curl -X POST https://your-backend-url/api/analyze \
  -F "text=SHOCKING: Doctors hate this trick!" \
  -F "language=en"
```

### Test Frontend
1. Visit: `https://said-eb2f5.web.app`
2. Enter fake news: "SHOCKING: Doctors hate this trick!"
3. Should show: ❌ **FAKE** with ML confidence
4. Test TTS: Click 🔊 Speak Results
5. Test OCR: Upload news image

## 📊 Expected Results

### For Fake News:
```
🤖 ML Model Prediction
Model: Trained Kaggle Model
Prediction: FAKE
ML Confidence: 85.2%

🧠 AI Explanation
This content shows characteristics of misinformation...
```

### For Real News:
```
🤖 ML Model Prediction
Model: Trained Kaggle Model
Prediction: REAL
ML Confidence: 78.9%

🧠 AI Explanation
This appears to be legitimate news content...
```

## 🔍 Troubleshooting

### Common Issues

1. **"API_BASE_URL not defined"**
   - Hard refresh browser: `Ctrl+Shift+R`
   - Check line 287 in `public/index.html`

2. **CORS Errors**
   - Update CORS origins in `app.py`
   - Redeploy backend

3. **Build Fails**
   ```bash
   gcloud builds log --region=us-central1
   ```

4. **ML Models Not Loading**
   - Check if `.pkl` files are in root directory
   - Verify file sizes (should be ~50MB total)

## 💰 Cost (Very Low)

- **Cloud Run**: Free tier covers 2M requests/month
- **Firebase**: Free tier covers 10GB transfer/month
- **Estimated**: $0-5/month for moderate usage

## 🎉 Success Checklist

After deployment, verify:
- ✅ Frontend loads at `https://said-eb2f5.web.app`
- ✅ Backend responds at `/api/health`
- ✅ Fake news shows as FAKE
- ✅ Real news shows as REAL
- ✅ TTS works without errors
- ✅ OCR extracts text from images
- ✅ Multiple languages work

## 🔄 Future Updates

### Update Backend
```bash
# Make code changes
git add . && git commit -m "Update"
gcloud builds submit --config cloudbuild.yaml
```

### Update Frontend
```bash
# Make UI changes
git add . && git commit -m "Update"
firebase deploy --only hosting
```

## 📱 Final URLs

After successful deployment:
- **Main App**: `https://said-eb2f5.web.app`
- **Backend API**: `https://truthlens-backend-XXXXX-uc.a.run.app`
- **Alternative**: `https://said-eb2f5.firebaseapp.com`

**Your ML-powered fake news detection system is now live on Google Cloud! 🎯**
