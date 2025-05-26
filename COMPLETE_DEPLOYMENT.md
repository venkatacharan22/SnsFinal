# 🚀 COMPLETE DEPLOYMENT GUIDE - TruthLens AI

## 📋 **STEP-BY-STEP INSTRUCTIONS FOR GOOGLE CLOUD SHELL**

### **🔥 COPY AND PASTE THESE COMMANDS:**

```bash
# 1. Clone the repository
git clone https://github.com/venkatacharan22/SnsFinal.git
cd SnsFinal

# 2. Set your Google Cloud project
gcloud config set project said-eb2f5

# 3. Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 4. Deploy backend to Cloud Run
echo "🚀 Deploying backend to Cloud Run..."
gcloud run deploy truthlens-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --port 8080 \
  --set-env-vars="FLASK_ENV=production"

# 5. Get the backend URL (save this!)
echo "📝 Getting backend URL..."
BACKEND_URL=$(gcloud run services describe truthlens-backend --region=us-central1 --format='value(status.url)')
echo "🌐 Backend URL: $BACKEND_URL"

# 6. Update frontend with backend URL
echo "🔧 Updating frontend with backend URL..."
sed -i "s|https://truthlens-backend-\[hash\]-us-central1.a.run.app|$BACKEND_URL|g" public/index.html

# 7. Deploy frontend to Firebase
echo "🔥 Deploying frontend to Firebase..."
firebase login --no-localhost
firebase use sns01-a8fba
firebase deploy --only hosting

echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 Your application URLs:"
echo "   Frontend: https://sns01-a8fba.web.app"
echo "   Backend:  $BACKEND_URL"
echo ""
echo "✨ Features now working:"
echo "   ✅ All 23 languages"
echo "   ✅ Real Gemini AI analysis"
echo "   ✅ Text-to-speech in all languages"
echo "   ✅ Image upload & analysis"
echo "   ✅ Mobile responsive design"
```

## 🧪 **TEST EXAMPLES AFTER DEPLOYMENT:**

### **Hindi (हिंदी):**
```
तत्काल: नासा ने पुष्टि की है कि पृथ्वी पर 15 दिन तक अंधकार रहेगा ग्रहों की स्थिति के कारण!
```

### **Tamil (தமிழ்):**
```
அதிர்ச்சி: நாசா உறுதிப்படுத்தியுள்ளது - கிரக சீரமைப்பு காரணமாக பூமியில் 15 நாட்கள் இருள் நிலவும்!
```

### **English:**
```
Breaking: NASA confirms Earth will experience darkness for 15 days due to planetary alignment!
```

## 🔧 **WHAT WILL WORK:**

✅ **Multilingual Analysis**: All 23 languages with proper responses
✅ **Text-to-Speech**: Voice output in Hindi, Tamil, Telugu, English, etc.
✅ **Image Analysis**: Upload news screenshots for verification
✅ **Real AI**: Actual Gemini 2.0 Flash model responses
✅ **Mobile Responsive**: Perfect on phones and tablets
✅ **Fast Performance**: Cloud Run auto-scaling

## 🆘 **TROUBLESHOOTING:**

### If backend deployment fails:
```bash
# Check logs
gcloud run logs read --service=truthlens-backend --region=us-central1

# Redeploy
gcloud run deploy truthlens-backend --source . --region us-central1 --allow-unauthenticated
```

### If frontend doesn't connect:
```bash
# Check backend URL
gcloud run services describe truthlens-backend --region=us-central1 --format='value(status.url)'

# Update frontend manually
nano public/index.html
# Find line 360 and replace with your backend URL

# Redeploy frontend
firebase deploy --only hosting
```

### Test backend directly:
```bash
# Health check
curl https://your-backend-url.com/api/health

# Test analysis
curl -X POST https://your-backend-url.com/api/analyze \
  -F "text=Breaking news test" \
  -F "language=en"
```

## 📊 **MONITORING:**

- **Backend Logs**: `gcloud run logs read --service=truthlens-backend --region=us-central1`
- **Frontend Analytics**: Firebase Console
- **Performance**: Cloud Run Console

## 🎯 **FINAL RESULT:**

After running these commands, you'll have:

1. **Backend**: Deployed on Google Cloud Run with auto-scaling
2. **Frontend**: Deployed on Firebase Hosting with global CDN
3. **Full Functionality**: All 23 languages, TTS, image analysis
4. **Production Ready**: HTTPS, fast loading, mobile optimized

**Frontend URL**: https://sns01-a8fba.web.app
**Backend URL**: Will be shown after deployment

---

**🚀 Ready to deploy? Copy the commands above to your Google Cloud Shell!**
