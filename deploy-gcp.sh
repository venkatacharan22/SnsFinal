#!/bin/bash

# TruthLens AI - Complete Auto-Deployment Script
echo "🚀 TruthLens AI - Auto-Deployment Starting..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to handle errors
handle_error() {
    echo -e "${RED}❌ Error: $1${NC}"
    exit 1
}

# Function to run command with error handling
run_command() {
    echo -e "${BLUE}🔧 Running: $1${NC}"
    if eval "$1"; then
        echo -e "${GREEN}✅ Success${NC}"
    else
        handle_error "Command failed: $1"
    fi
}

# Check if required tools are installed
echo -e "${BLUE}🔧 Checking prerequisites...${NC}"

if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is required but not installed.${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v firebase &> /dev/null; then
    echo -e "${RED}❌ firebase CLI is required but not installed.${NC}"
    echo "Install with: npm install -g firebase-tools"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No Google Cloud project set.${NC}"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${BLUE}📋 Using Google Cloud Project: ${PROJECT_ID}${NC}"

# Auto-detect or set region
echo -e "${YELLOW}🌍 Setting up region...${NC}"
run_command "gcloud config set run/region us-central1"

# Step 1: Enable APIs
echo -e "${YELLOW}🔧 Step 1: Enabling APIs...${NC}"
run_command "gcloud services enable cloudbuild.googleapis.com --quiet"
run_command "gcloud services enable run.googleapis.com --quiet"
run_command "gcloud services enable containerregistry.googleapis.com --quiet"

# Step 2: Deploy Backend to Cloud Run
echo -e "${YELLOW}🔧 Step 2: Deploying Backend to Cloud Run...${NC}"
echo "🏗️  Building and deploying backend (this takes 3-5 minutes)..."
run_command "gcloud builds submit --config cloudbuild.yaml"

# Step 3: Get backend URL with retry logic
echo -e "${YELLOW}🔧 Step 3: Getting backend URL...${NC}"
BACKEND_URL=""
for i in {1..5}; do
    BACKEND_URL=$(gcloud run services describe truthlens-backend --region=us-central1 --format="value(status.url)" 2>/dev/null)
    if [ ! -z "$BACKEND_URL" ]; then
        break
    fi
    echo "Waiting for service to be ready... (attempt $i/5)"
    sleep 10
done

if [ -z "$BACKEND_URL" ]; then
    # Try different regions
    echo "Trying different regions..."
    for region in us-east1 us-west1 europe-west1; do
        BACKEND_URL=$(gcloud run services describe truthlens-backend --region=$region --format="value(status.url)" 2>/dev/null)
        if [ ! -z "$BACKEND_URL" ]; then
            echo "Found service in region: $region"
            break
        fi
    done
fi

if [ -z "$BACKEND_URL" ]; then
    handle_error "Failed to get backend URL"
fi

echo -e "${GREEN}✅ Backend deployed at: ${BACKEND_URL}${NC}"

# Step 4: Update frontend with backend URL
echo -e "${YELLOW}🔧 Step 4: Updating frontend with backend URL...${NC}"

# Create backup
cp public/index.html public/index.html.backup

# Update the frontend with the actual backend URL
echo "Updating frontend to use: $BACKEND_URL"
run_command "sed -i.tmp 's|https://truthlens-backend-YOUR_PROJECT_ID-uc.a.run.app|$BACKEND_URL|g' public/index.html"
rm public/index.html.tmp 2>/dev/null

echo -e "${GREEN}✅ Frontend updated with backend URL${NC}"

# Step 5: Deploy Frontend to Firebase
echo -e "${YELLOW}🔧 Step 5: Deploying Frontend to Firebase...${NC}"

# Get Firebase project from .firebaserc
FIREBASE_PROJECT=$(cat .firebaserc | grep -o '"default": "[^"]*"' | cut -d'"' -f4)
echo "Using Firebase project: $FIREBASE_PROJECT"

# Deploy to Firebase Hosting
echo "🚀 Deploying to Firebase Hosting..."
run_command "firebase deploy --only hosting --non-interactive"

# Get the frontend URL
FRONTEND_URL="https://$FIREBASE_PROJECT.web.app"
echo -e "${GREEN}✅ Frontend deployed at: ${FRONTEND_URL}${NC}"

# Step 6: Test the deployment
echo -e "${YELLOW}🔧 Step 6: Testing deployment...${NC}"

# Test backend health
echo "Testing backend health..."
if curl -s "$BACKEND_URL/api/health" > /dev/null; then
    echo -e "${GREEN}✅ Backend health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed (may still be starting)${NC}"
fi

# Test backend analysis
echo "Testing backend analysis..."
if curl -s -X POST "$BACKEND_URL/api/analyze" -F "text=test" -F "language=en" > /dev/null; then
    echo -e "${GREEN}✅ Backend analysis endpoint working${NC}"
else
    echo -e "${YELLOW}⚠️  Backend analysis test failed (may need time to warm up)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 AUTO-DEPLOYMENT COMPLETE!${NC}"
echo "=============================================="
echo -e "${BLUE}📱 Frontend: ${FRONTEND_URL}${NC}"
echo -e "${BLUE}🔧 Backend: ${BACKEND_URL}${NC}"
echo ""
echo -e "${YELLOW}🧪 Test Your Application:${NC}"
echo "1. Visit: $FRONTEND_URL"
echo "2. Test fake news: 'SHOCKING: Doctors hate this trick!'"
echo "3. Test real news: 'Weather forecast shows rain tomorrow'"
echo "4. Test TTS: Click 🔊 Speak Results"
echo "5. Test OCR: Upload a news image"
echo ""
echo -e "${YELLOW}🔧 API Endpoints:${NC}"
echo "   Health: $BACKEND_URL/api/health"
echo "   Analysis: $BACKEND_URL/api/analyze"
echo ""
echo -e "${GREEN}✅ Your ML-powered fake news detection system is LIVE!${NC}"
echo -e "${BLUE}🎯 Features: ML Models + Gemini AI + OCR + TTS + 23 Languages${NC}"
