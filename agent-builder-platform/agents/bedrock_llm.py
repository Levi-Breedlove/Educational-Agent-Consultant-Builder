"""
AWS Bedrock LLM Service
Connects agents to Claude via AWS Bedrock
"""

import boto3
import json
import logging
import os
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BedrockLLMService:
    """AWS Bedrock Claude integration for local testing"""
    
    def __init__(
        self, 
        region_name: str = None,
        model_id: str = None
    ):
        """
        Initialize Bedrock client
        
        Args:
            region_name: AWS region (default: us-east-1)
            model_id: Claude model ID (default: Claude 3 Sonnet)
        """
        self.region_name = region_name or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.model_id = model_id or "anthropic.claude-3-sonnet-20240229-v1:0"
        
        # Initialize Bedrock client
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region_name
            )
            logger.info(f"✅ Bedrock client initialized in {self.region_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Bedrock client: {e}")
            raise
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate response using Claude via Bedrock
        
        Args:
            prompt: User prompt/question
            system_prompt: System instructions for Claude
            max_tokens: Maximum tokens in response
            temperature: Randomness (0-1)
            top_p: Nucleus sampling parameter
            
        Returns:
            Claude's response text
        """
        try:
            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Prepare request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "messages": messages
            }
            
            # Add system prompt if provided
            if system_prompt:
                request_body["system"] = system_prompt
            
            # Log request (truncated)
            logger.info(f"🤖 Calling Bedrock Claude...")
            logger.debug(f"Model: {self.model_id}")
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            # Call Bedrock
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text
            if 'content' in response_body and len(response_body['content']) > 0:
                response_text = response_body['content'][0]['text']
                logger.info(f"✅ Received response ({len(response_text)} chars)")
                return response_text
            else:
                logger.error("❌ No content in response")
                return "Error: No response from Claude"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            logger.error(f"❌ Bedrock API error: {error_code} - {error_message}")
            
            # Provide helpful error messages
            if error_code == 'AccessDeniedException':
                return "Error: Access denied. Please check:\n1. AWS credentials are correct\n2. IAM permissions include bedrock:InvokeModel\n3. Model access is enabled in Bedrock console"
            elif error_code == 'ResourceNotFoundException':
                return f"Error: Model not found. Please check:\n1. Model ID is correct: {self.model_id}\n2. Model is available in region: {self.region_name}"
            elif error_code == 'ThrottlingException':
                return "Error: Rate limit exceeded. Please wait and try again."
            else:
                return f"Error: {error_message}"
                
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test Bedrock connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Simple test prompt
            test_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say 'Connection successful' if you can read this."
                    }
                ]
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(test_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body:
                logger.info("✅ Bedrock connection test successful")
                return True
            else:
                logger.error("❌ Bedrock connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Bedrock connection test failed: {e}")
            return False

# Global instance (lazy initialization)
_bedrock_llm = None

def get_bedrock_llm() -> BedrockLLMService:
    """Get or create Bedrock LLM service instance"""
    global _bedrock_llm
    if _bedrock_llm is None:
        _bedrock_llm = BedrockLLMService()
    return _bedrock_llm
