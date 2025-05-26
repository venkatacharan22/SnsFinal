#!/bin/bash

echo "🚀 Deploying TruthLens AI Backend to Google Cloud Run"
echo "=================================================="

# Set project ID
PROJECT_ID="said-eb2f5"
SERVICE_NAME="truthlens-backend"
REGION="us-central1"

echo "📋 Project ID: $PROJECT_ID"
echo "🔧 Service Name: $SERVICE_NAME"
echo "🌍 Region: $REGION"

# Set the project
gcloud config set project $PROJECT_ID

# Build and deploy to Cloud Run
echo "🔨 Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --port 8080 \
  --set-env-vars="FLASK_ENV=production"

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your backend will be available at:"
echo "   https://$SERVICE_NAME-[hash]-$REGION.a.run.app"
echo ""
echo "📝 Next steps:"
echo "1. Copy the backend URL from the output above"
echo "2. Update the frontend with the new backend URL"
echo "3. Redeploy to Firebase"
