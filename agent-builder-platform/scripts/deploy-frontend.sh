#!/bin/bash

# Deploy frontend to S3 and invalidate CloudFront cache
# Requirements: 12.2

set -e

# Configuration
PROJECT_NAME="${PROJECT_NAME:-agent-builder}"
ENVIRONMENT="${ENVIRONMENT:-dev}"
REGION="${AWS_REGION:-us-east-1}"
FRONTEND_DIR="frontend/dist"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Frontend${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Project: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    exit 1
fi

# Check if frontend build exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${YELLOW}Frontend build not found. Building...${NC}"
    cd frontend
    npm run build
    cd ..
fi

# Get S3 bucket name
FRONTEND_BUCKET="${PROJECT_NAME}-${ENVIRONMENT}-frontend"

# Sync files to S3
echo -e "${GREEN}Uploading files to S3...${NC}"

# Upload HTML files (no cache)
aws s3 sync "$FRONTEND_DIR" "s3://${FRONTEND_BUCKET}" \
    --exclude "*" \
    --include "*.html" \
    --cache-control "no-cache, no-store, must-revalidate" \
    --metadata-directive REPLACE \
    --region "$REGION"

# Upload service worker (no cache)
aws s3 sync "$FRONTEND_DIR" "s3://${FRONTEND_BUCKET}" \
    --exclude "*" \
    --include "sw.js" \
    --cache-control "no-cache, no-store, must-revalidate" \
    --metadata-directive REPLACE \
    --region "$REGION"

# Upload manifest (short cache)
aws s3 sync "$FRONTEND_DIR" "s3://${FRONTEND_BUCKET}" \
    --exclude "*" \
    --include "manifest.json" \
    --cache-control "public, max-age=3600" \
    --metadata-directive REPLACE \
    --region "$REGION"

# Upload static assets (long cache with immutable)
aws s3 sync "$FRONTEND_DIR/assets" "s3://${FRONTEND_BUCKET}/assets" \
    --cache-control "public, max-age=31536000, immutable" \
    --metadata-directive REPLACE \
    --region "$REGION"

# Upload other files (medium cache)
aws s3 sync "$FRONTEND_DIR" "s3://${FRONTEND_BUCKET}" \
    --exclude "*.html" \
    --exclude "sw.js" \
    --exclude "manifest.json" \
    --exclude "assets/*" \
    --cache-control "public, max-age=86400" \
    --metadata-directive REPLACE \
    --region "$REGION"

echo -e "${GREEN}Files uploaded successfully${NC}"

# Get CloudFront distribution ID
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}-cdn"
DISTRIBUTION_ID=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`DistributionId`].OutputValue' \
    --output text 2>/dev/null || echo "")

if [ -n "$DISTRIBUTION_ID" ]; then
    echo -e "${GREEN}Invalidating CloudFront cache...${NC}"
    
    INVALIDATION_ID=$(aws cloudfront create-invalidation \
        --distribution-id "$DISTRIBUTION_ID" \
        --paths "/*" \
        --query 'Invalidation.Id' \
        --output text)
    
    echo "Invalidation ID: $INVALIDATION_ID"
    echo -e "${YELLOW}Cache invalidation in progress (may take 5-10 minutes)${NC}"
    
    # Get distribution domain
    DISTRIBUTION_DOMAIN=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`DistributionDomainName`].OutputValue' \
        --output text)
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Frontend Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Frontend URL: https://$DISTRIBUTION_DOMAIN"
    echo "S3 Bucket: s3://$FRONTEND_BUCKET"
    echo ""
else
    echo -e "${YELLOW}CloudFront distribution not found. Skipping cache invalidation.${NC}"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Frontend Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "S3 Bucket: s3://$FRONTEND_BUCKET"
    echo "S3 Website URL: http://${FRONTEND_BUCKET}.s3-website-${REGION}.amazonaws.com"
    echo ""
fi

# Calculate and display bundle sizes
echo -e "${GREEN}Bundle Sizes:${NC}"
du -sh "$FRONTEND_DIR"
echo ""
echo "Detailed breakdown:"
du -sh "$FRONTEND_DIR"/* | sort -h
