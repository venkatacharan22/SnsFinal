# 🚀 Complete Google Cloud Deployment Guide

## 📋 **Step-by-Step Instructions**

### **Step 1: Clone Repository in Cloud Shell**

In your Google Cloud Shell, run:

```bash
# Clone the repository
git clone https://github.com/venkatacharan22/SnsFinal.git
cd SnsFinal

# Verify files
ls -la
```

### **Step 2: Enable Required APIs**

```bash
# Enable necessary Google Cloud APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Set your project (already done)
gcloud config set project said-eb2f5
```

### **Step 3: Deploy Backend to Cloud Run**

```bash
# Deploy the Flask backend
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
```

### **Step 4: Get Backend URL**

After deployment, you'll get a URL like:
```
https://truthlens-backend-[hash]-us-central1.a.run.app
```

**COPY THIS URL** - you'll need it for the next step!

### **Step 5: Update Frontend with Backend URL**

```bash
# Edit the frontend file
nano public/index.html
```

Find this line (around line 361):
```javascript
: 'https://your-backend-url.com'; // Replace with your actual backend URL
```

Replace it with your actual Cloud Run URL:
```javascript
: 'https://truthlens-backend-[your-hash]-us-central1.a.run.app';
```

Save the file (Ctrl+X, then Y, then Enter)

### **Step 6: Redeploy Frontend to Firebase**

```bash
# Login to Firebase (if needed)
firebase login --no-localhost

# Use your Firebase project
firebase use sns01-a8fba

# Deploy updated frontend
firebase deploy --only hosting
```

## 🎉 **Final Result**

Your complete application will be available at:
- **Frontend**: https://sns01-a8fba.web.app
- **Backend**: https://truthlens-backend-[hash]-us-central1.a.run.app

## ✨ **What Will Work:**

✅ **All 23 Languages** - Full multilingual support
✅ **Real Gemini AI Analysis** - Actual AI-powered fact checking
✅ **Text-to-Speech** - Voice output in all languages
✅ **Image Upload** - Analyze news screenshots
✅ **Mobile Responsive** - Perfect on all devices
✅ **Real-time Analysis** - Live fact checking

## 🧪 **Test Examples:**

### Hindi
```
तत्काल: नासा ने पुष्टि की है कि पृथ्वी पर 15 दिन तक अंधकार रहेगा!
```

### Tamil
```
அதிர்ச்சி: நாசா உறுதிப்படுத்தியுள்ளது - கிரக சீரமைப்பு காரணமாக பூமியில் 15 நாட்கள் இருள் நிலவும்!
```

### English
```
Breaking: NASA confirms Earth will experience darkness for 15 days!
```

## 🔧 **Troubleshooting:**

### If deployment fails:
```bash
# Check logs
gcloud run logs read --service=truthlens-backend --region=us-central1

# Redeploy if needed
gcloud run deploy truthlens-backend --source . --region us-central1 --allow-unauthenticated
```

### If frontend doesn't connect:
1. Verify the backend URL is correct in `public/index.html`
2. Check CORS settings in the backend
3. Redeploy frontend: `firebase deploy --only hosting`

## 📊 **Monitoring:**

- **Cloud Run Console**: https://console.cloud.google.com/run
- **Firebase Console**: https://console.firebase.google.com/project/sns01-a8fba
- **Backend Health**: https://your-backend-url.com/api/health

---

**Ready to deploy? Copy these commands to your Cloud Shell!** 🚀
