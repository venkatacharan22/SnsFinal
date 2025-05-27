# 🚀 AUTO-DEPLOY YOUR ML FAKE NEWS DETECTION SYSTEM

## 🎯 ONE COMMAND TO DEPLOY EVERYTHING

```bash
cd /Users/asha/Semester\ 6/SNS-1
./deploy-gcp.sh
```

**That's it! The script will automatically:**

✅ **Deploy Backend** → Cloud Run (ML models + Gemini AI)  
✅ **Deploy Frontend** → Firebase Hosting (responsive UI)  
✅ **Update API URLs** → Connect frontend to backend  
✅ **Test Everything** → Verify all endpoints work  
✅ **Provide URLs** → Ready-to-use application links  

## ⏱️ **Timeline: ~5-7 minutes**

- **APIs setup**: 30 seconds
- **Backend build**: 3-5 minutes  
- **Frontend deploy**: 1 minute
- **Testing**: 30 seconds

## 📱 **What You'll Get**

### **Frontend URL**: `https://sns01-a8fba.web.app`
- Beautiful responsive UI ✨
- 23 language support 🌍
- Mobile-friendly design 📱

### **Backend URL**: `https://truthlens-backend-XXXXX-uc.a.run.app`
- Real ML models (Kaggle-trained) 🤖
- Gemini AI explanations 🧠
- OCR text extraction 📷
- Text-to-speech 🔊

## 🧪 **Test Examples**

### **Fake News** (should show ❌ FAKE):
```
SHOCKING: Doctors hate this one weird trick that cures everything!
```

### **Real News** (should show ✅ REAL):
```
Local weather forecast shows rain expected tomorrow according to meteorological department.
```

## 🎉 **Features Live**

- ✅ **ML Predictions** → Real machine learning models
- ✅ **AI Explanations** → Gemini AI in 23 languages  
- ✅ **Image OCR** → Extract text from news screenshots
- ✅ **Text-to-Speech** → Voice output in multiple languages
- ✅ **Mobile Ready** → Works on all devices
- ✅ **Global CDN** → Fast worldwide access

## 🔧 **If Something Goes Wrong**

The script has built-in error handling, but if needed:

```bash
# Check Cloud Run services
gcloud run services list

# Check Firebase projects  
firebase projects:list

# Manual backend deploy
gcloud builds submit --config cloudbuild.yaml

# Manual frontend deploy
firebase deploy --only hosting
```

## 💰 **Cost: FREE**

- **Cloud Run**: Free tier (2M requests/month)
- **Firebase**: Free tier (10GB transfer/month)
- **Estimated**: $0-5/month for moderate usage

---

# 🎯 **READY TO DEPLOY?**

**Just run this one command:**

```bash
./deploy-gcp.sh
```

**Your complete ML-powered fake news detection system will be live in ~5 minutes!** 🚀
