#!/bin/bash

echo "🚀 TruthLens AI Firebase Deployment Script"
echo "=========================================="

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

echo "✅ Firebase CLI is ready"

# Login to Firebase (if not already logged in)
echo "🔐 Checking Firebase authentication..."
firebase login --no-localhost

# List available projects
echo "📋 Available Firebase projects:"
firebase projects:list

echo ""
echo "📝 Please follow these steps:"
echo "1. Update .firebaserc with your project ID"
echo "2. Run: firebase use your-project-id"
echo "3. Run: firebase deploy"
echo ""
echo "🔧 For backend deployment, consider using:"
echo "   - Google Cloud Functions"
echo "   - Google Cloud Run"
echo "   - Heroku"
echo "   - Railway"
echo ""
echo "📱 Your frontend will be available at:"
echo "   https://your-project-id.web.app"
echo "   https://your-project-id.firebaseapp.com"
