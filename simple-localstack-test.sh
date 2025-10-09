#!/bin/bash

# Simple LocalStack Test - Safe AWS Simulation
echo "🐳 Starting Simple LocalStack Test"
echo "=================================="

# Set LocalStack environment variables
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

echo "✅ LocalStack environment configured"
echo "  AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "  AWS_ENDPOINT_URL: $AWS_ENDPOINT_URL"

# Start LocalStack with Docker
echo
echo "🚀 Starting LocalStack container..."
docker run -d \
  --name agent-builder-localstack \
  -p 4566:4566 \
  -e SERVICES=s3,dynamodb,ecs,iam,cloudformation,sns,events,logs \
  -e DEBUG=1 \
  localstack/localstack:latest

# Wait for LocalStack to start
echo "⏳ Waiting for LocalStack to be ready..."
sleep 15

# Test LocalStack health
echo "🔍 Testing LocalStack health..."
if curl -s http://localhost:4566/health | grep -q "running"; then
    echo "✅ LocalStack is running and healthy"
else
    echo "⚠️  LocalStack may still be starting up"
fi

# Test AWS CLI with LocalStack
echo
echo "🧪 Testing AWS CLI with LocalStack..."

# Test S3
echo "Testing S3..."
if aws --endpoint-url=http://localhost:4566 s3 mb s3://test-bucket 2>/dev/null; then
    echo "✅ S3 test passed"
else
    echo "⚠️  S3 test failed (LocalStack may still be starting)"
fi

# Test DynamoDB
echo "Testing DynamoDB..."
if aws --endpoint-url=http://localhost:4566 dynamodb list-tables 2>/dev/null; then
    echo "✅ DynamoDB test passed"
else
    echo "⚠️  DynamoDB test failed (LocalStack may still be starting)"
fi

# Test CloudFormation template validation
echo "Testing CloudFormation template..."
if aws --endpoint-url=http://localhost:4566 cloudformation validate-template \
   --template-body file://agent-builder-platform/infrastructure/main-stack.yaml 2>/dev/null; then
    echo "✅ CloudFormation template validation passed"
else
    echo "⚠️  CloudFormation template validation failed"
fi

echo
echo "🎯 LocalStack Test Summary:"
echo "  • LocalStack container started"
echo "  • AWS CLI configured for LocalStack"
echo "  • Basic service tests completed"
echo "  • Your real AWS account is completely safe"
echo
echo "💰 Cost: $0.00 - Completely free simulation"

# Cleanup function
cleanup() {
    echo
    echo "🧹 Cleaning up LocalStack..."
    docker stop agent-builder-localstack 2>/dev/null
    docker rm agent-builder-localstack 2>/dev/null
    echo "✅ Cleanup completed"
}

# Set trap for cleanup on exit
trap cleanup EXIT

echo
echo "LocalStack is running. Press Ctrl+C to stop and cleanup."
echo "Container will auto-cleanup when script exits."

# Keep script running
sleep 30