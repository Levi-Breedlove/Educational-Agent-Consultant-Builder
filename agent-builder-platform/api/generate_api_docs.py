#!/usr/bin/env python3
"""
API Documentation Generator
Generates comprehensive API documentation including OpenAPI spec, examples, and guides
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.main import app
from api.openapi_enhancements import (
    API_METADATA, ENDPOINT_EXAMPLES, RESPONSE_EXAMPLES, ERROR_EXAMPLES
)


def generate_openapi_spec() -> Dict[str, Any]:
    """Generate enhanced OpenAPI specification"""
    # Get base OpenAPI schema from FastAPI
    openapi_schema = app.openapi()
    
    # Enhance with custom metadata
    openapi_schema.update({
        "info": {
            **openapi_schema.get("info", {}),
            **API_METADATA
        }
    })
    
    # Add enhanced examples to endpoints
    if "paths" in openapi_schema:
        for path, methods in openapi_schema["paths"].items():
            for method, details in methods.items():
                # Add request examples
                if "requestBody" in details:
                    operation_id = details.get("operationId", "")
                    if operation_id in ENDPOINT_EXAMPLES:
                        examples = ENDPOINT_EXAMPLES[operation_id].get("examples", {})
                        if examples and "content" in details["requestBody"]:
                            for content_type in details["requestBody"]["content"]:
                                details["requestBody"]["content"][content_type]["examples"] = examples
                
                # Add response examples
                if "responses" in details:
                    for status_code, response in details["responses"].items():
                        if status_code == "200" and "content" in response:
                            for content_type in response["content"]:
                                if "examples" not in response["content"][content_type]:
                                    response["content"][content_type]["examples"] = RESPONSE_EXAMPLES
    
    return openapi_schema


def generate_markdown_docs() -> str:
    """Generate markdown documentation"""
    docs = []
    
    # Header
    docs.append("# Agent Builder Platform API Documentation\n")
    docs.append(f"**Version:** {API_METADATA['version']}\n")
    docs.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    docs.append("\n---\n")
    
    # Overview
    docs.append("## Overview\n")
    docs.append(API_METADATA['description'])
    docs.append("\n")
    
    # Authentication
    docs.append("## Authentication\n")
    docs.append("The API uses session-based authentication. Create a session using the `/api/sessions` endpoint ")
    docs.append("and use the returned `session_id` for subsequent requests.\n\n")
    docs.append("For production deployments, JWT token authentication is available.\n")
    docs.append("\n")
    
    # Endpoints
    docs.append("## Endpoints\n")
    
    openapi_schema = app.openapi()
    
    # Group endpoints by tags
    endpoints_by_tag = {}
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            tags = details.get("tags", ["Untagged"])
            for tag in tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append({
                    "path": path,
                    "method": method.upper(),
                    "details": details
                })
    
    # Document each tag group
    for tag, endpoints in sorted(endpoints_by_tag.items()):
        docs.append(f"### {tag}\n")
        
        for endpoint in endpoints:
            path = endpoint["path"]
            method = endpoint["method"]
            details = endpoint["details"]
            
            docs.append(f"#### `{method} {path}`\n")
            docs.append(f"{details.get('summary', 'No summary')}\n\n")
            
            if "description" in details:
                docs.append(f"{details['description']}\n\n")
            
            # Parameters
            if "parameters" in details:
                docs.append("**Parameters:**\n")
                for param in details["parameters"]:
                    required = " (required)" if param.get("required") else " (optional)"
                    docs.append(f"- `{param['name']}`{required}: {param.get('description', 'No description')}\n")
                docs.append("\n")
            
            # Request body
            if "requestBody" in details:
                docs.append("**Request Body:**\n")
                docs.append("```json\n")
                # Get example from schema
                content = details["requestBody"].get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    if "example" in schema:
                        docs.append(json.dumps(schema["example"], indent=2))
                    else:
                        docs.append("{\n  // See API documentation for schema\n}")
                docs.append("\n```\n\n")
            
            # Responses
            if "responses" in details:
                docs.append("**Responses:**\n")
                for status_code, response in details["responses"].items():
                    description = response.get("description", "No description")
                    docs.append(f"- `{status_code}`: {description}\n")
                docs.append("\n")
            
            docs.append("---\n\n")
    
    # Error Codes
    docs.append("## Error Codes\n")
    docs.append("| Code | Description |\n")
    docs.append("|------|-------------|\n")
    docs.append("| 200 | Success |\n")
    docs.append("| 201 | Created |\n")
    docs.append("| 400 | Bad Request - Invalid input |\n")
    docs.append("| 404 | Not Found - Resource doesn't exist |\n")
    docs.append("| 422 | Unprocessable Entity - Validation error |\n")
    docs.append("| 500 | Internal Server Error |\n")
    docs.append("\n")
    
    # Rate Limiting
    docs.append("## Rate Limiting\n")
    docs.append("- Default: 100 requests per minute per session\n")
    docs.append("- Burst: 200 requests per minute\n")
    docs.append("- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`\n")
    docs.append("\n")
    
    # Examples
    docs.append("## Example Workflows\n")
    docs.append("### Complete Agent Creation Workflow\n")
    docs.append("```bash\n")
    docs.append("# 1. Create a session\n")
    docs.append('curl -X POST http://localhost:8000/api/sessions \\\n')
    docs.append('  -H "Content-Type: application/json" \\\n')
    docs.append('  -d \'{"experience_level": "beginner"}\'\n\n')
    docs.append("# 2. Create an agent\n")
    docs.append('curl -X POST http://localhost:8000/api/agents/create \\\n')
    docs.append('  -H "Content-Type: application/json" \\\n')
    docs.append('  -d \'{\n')
    docs.append('    "session_id": "session-abc-123",\n')
    docs.append('    "use_case": "customer_support_chatbot",\n')
    docs.append('    "description": "Build an AI chatbot for customer support"\n')
    docs.append('  }\'\n\n')
    docs.append("# 3. Check status\n")
    docs.append('curl http://localhost:8000/api/agents/agent-xyz-789/status\n\n')
    docs.append("# 4. Export agent\n")
    docs.append('curl http://localhost:8000/api/agents/agent-xyz-789/export?export_format=complete\n')
    docs.append("```\n\n")
    
    return "".join(docs)


def generate_postman_collection() -> Dict[str, Any]:
    """Generate Postman collection for API testing"""
    collection = {
        "info": {
            "name": "Agent Builder Platform API",
            "description": API_METADATA['description'],
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": [
            {
                "key": "baseUrl",
                "value": "http://localhost:8000",
                "type": "string"
            },
            {
                "key": "session_id",
                "value": "",
                "type": "string"
            },
            {
                "key": "agent_id",
                "value": "",
                "type": "string"
            }
        ]
    }
    
    openapi_schema = app.openapi()
    
    # Convert OpenAPI paths to Postman requests
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            request = {
                "name": details.get("summary", path),
                "request": {
                    "method": method.upper(),
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "url": {
                        "raw": "{{baseUrl}}" + path,
                        "host": ["{{baseUrl}}"],
                        "path": path.strip("/").split("/")
                    }
                },
                "response": []
            }
            
            # Add request body if present
            if "requestBody" in details:
                content = details["requestBody"].get("content", {})
                if "application/json" in content:
                    schema = content["application/json"].get("schema", {})
                    if "example" in schema:
                        request["request"]["body"] = {
                            "mode": "raw",
                            "raw": json.dumps(schema["example"], indent=2)
                        }
            
            collection["item"].append(request)
    
    return collection


def main():
    """Generate all documentation"""
    print("=" * 80)
    print("API DOCUMENTATION GENERATOR")
    print("=" * 80)
    print()
    
    output_dir = os.path.dirname(__file__)
    
    # Generate OpenAPI spec
    print("Generating OpenAPI specification...")
    openapi_spec = generate_openapi_spec()
    openapi_path = os.path.join(output_dir, "openapi.json")
    with open(openapi_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
    print(f"✓ OpenAPI spec saved to: {openapi_path}")
    
    # Generate Markdown docs
    print("Generating Markdown documentation...")
    markdown_docs = generate_markdown_docs()
    markdown_path = os.path.join(output_dir, "API-REFERENCE.md")
    with open(markdown_path, "w") as f:
        f.write(markdown_docs)
    print(f"✓ Markdown docs saved to: {markdown_path}")
    
    # Generate Postman collection
    print("Generating Postman collection...")
    postman_collection = generate_postman_collection()
    postman_path = os.path.join(output_dir, "postman_collection.json")
    with open(postman_path, "w") as f:
        json.dump(postman_collection, f, indent=2)
    print(f"✓ Postman collection saved to: {postman_path}")
    
    print()
    print("=" * 80)
    print("DOCUMENTATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Generated files:")
    print(f"  - {openapi_path}")
    print(f"  - {markdown_path}")
    print(f"  - {postman_path}")
    print()
    print("You can now:")
    print("  - View OpenAPI docs at: http://localhost:8000/api/docs")
    print("  - Import Postman collection for API testing")
    print("  - Read API-REFERENCE.md for detailed documentation")


if __name__ == "__main__":
    main()
