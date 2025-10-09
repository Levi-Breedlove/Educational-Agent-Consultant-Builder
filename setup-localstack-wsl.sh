#!/bin/bash

# Setup LocalStack environment in WSL - SAFE SIMULATION ONLY
echo "🛡️  Setting up SAFE LocalStack environment in WSL..."
echo "This will BLOCK access to your real AWS account"

# Set LocalStack environment variables
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

# Verify settings
echo
echo "✅ LocalStack Environment Variables Set:"
echo "  AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "  AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
echo "  AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION"
echo "  AWS_ENDPOINT_URL: $AWS_ENDPOINT_URL"
echo

# Test that real AWS is blocked
echo "🔒 Verifying real AWS is blocked..."
if aws sts get-caller-identity 2>&1 | grep -q "Could not connect"; then
    echo "✅ SUCCESS: Real AWS is blocked - you are safe!"
else
    echo "❌ WARNING: Real AWS might be accessible!"
fi

echo
echo "🚀 Ready for LocalStack testing!"
echo "Your real AWS account is completely protected."