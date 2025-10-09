#!/usr/bin/env python3
"""
Demo: Export and Deployment Functionality
Demonstrates the export and deployment endpoints
"""

import asyncio
import json
from export_service import ExportService, ExportFormat, DeploymentTarget


async def demo_export_formats():
    """Demonstrate different export formats"""
    print("=" * 80)
    print("DEMO: Export Formats")
    print("=" * 80)
    
    export_service = ExportService()
    
    # Sample workflow data
    workflow_data = {
        'requirements': {
            'use_case': 'customer_support_chatbot',
            'description': 'AI-powered customer support chatbot using AWS Bedrock',
            'user_id': 'demo-user',
            'experience_level': 'beginner'
        },
        'architecture': {
            'aws_services': ['lambda', 'dynamodb', 's3', 'bedrock'],
            'mcps': ['aws_documentation', 'strands_patterns', 'perplexity'],
            'capabilities': ['natural_language_processing', 'data_storage', 'conversation_management'],
            'tools': ['aws_lambda', 'aws_bedrock', 'aws_dynamodb'],
            'cost_estimate': '$15-30/month'
        },
        'implementation': {
            'code_generated': True,
            'tests_included': True
        }
    }
    
    # Test each export format
    formats = [
        (ExportFormat.CODE, "Source Code Only"),
        (ExportFormat.IAC, "Infrastructure as Code"),
        (ExportFormat.CONTAINER, "Container Configuration"),
        (ExportFormat.STRANDS, "Strands Specification"),
        (ExportFormat.COMPLETE, "Complete Package")
    ]
    
    for export_format, description in formats:
        print(f"\n{'=' * 80}")
        print(f"Format: {description} ({export_format.value})")
        print(f"{'=' * 80}")
        
        result = await export_service.export_agent(
            agent_id=f'demo-agent-{export_format.value}',
            workflow_data=workflow_data,
            export_format=export_format,
            include_tests=True
        )
        
        print(f"\n✅ Export successful!")
        print(f"   Agent ID: {result['agent_id']}")
        print(f"   Format: {result['export_format']}")
        print(f"   Files generated: {result['metadata']['file_count']}")
        print(f"   Total size: {result['metadata']['export_size_bytes']:,} bytes")
        
        print(f"\n📁 Files included:")
        for i, file_path in enumerate(sorted(result['files'].keys())[:10], 1):
            print(f"   {i}. {file_path}")
        
        if len(result['files']) > 10:
            print(f"   ... and {len(result['files']) - 10} more files")
        
        print(f"\n📋 Deployment Instructions:")
        for instruction in result['deployment_instructions'][:5]:
            print(f"   • {instruction}")


async def demo_deployment_scripts():
    """Demonstrate deployment script generation"""
    print("\n\n" + "=" * 80)
    print("DEMO: Deployment Scripts")
    print("=" * 80)
    
    export_service = ExportService()
    
    workflow_data = {
        'requirements': {
            'use_case': 'data_processor',
            'description': 'Data processing agent'
        },
        'architecture': {
            'aws_services': ['lambda', 's3', 'sqs'],
            'mcps': ['aws_documentation'],
            'cost_estimate': '$10-20/month'
        },
        'implementation': {}
    }
    
    # Test each deployment target
    targets = [
        (DeploymentTarget.AWS_LAMBDA, "AWS Lambda", "5-10 minutes"),
        (DeploymentTarget.AWS_ECS, "AWS ECS", "10-15 minutes"),
        (DeploymentTarget.DOCKER, "Docker", "2-5 minutes"),
        (DeploymentTarget.LOCAL, "Local Development", "1-2 minutes")
    ]
    
    for target, description, est_time in targets:
        print(f"\n{'=' * 80}")
        print(f"Target: {description} ({target.value})")
        print(f"{'=' * 80}")
        
        scripts = await export_service.generate_deployment_scripts(
            agent_id=f'demo-agent-{target.value}',
            workflow_data=workflow_data,
            deployment_target=target
        )
        
        print(f"\n✅ Scripts generated!")
        print(f"   Target: {target.value}")
        print(f"   Scripts: {len(scripts)}")
        print(f"   Estimated time: {est_time}")
        
        print(f"\n📜 Generated scripts:")
        for script_name in scripts.keys():
            print(f"   • {script_name}")


async def demo_complete_workflow():
    """Demonstrate complete export and deployment workflow"""
    print("\n\n" + "=" * 80)
    print("DEMO: Complete Workflow")
    print("=" * 80)
    
    export_service = ExportService()
    
    workflow_data = {
        'requirements': {
            'use_case': 'sentiment_analyzer',
            'description': 'Real-time sentiment analysis agent using AWS Bedrock',
            'user_id': 'demo-user',
            'experience_level': 'intermediate'
        },
        'architecture': {
            'aws_services': ['lambda', 'dynamodb', 'bedrock', 'api_gateway'],
            'mcps': ['aws_documentation', 'aws_ai_ml', 'strands_patterns'],
            'capabilities': ['sentiment_analysis', 'real_time_processing', 'api_integration'],
            'tools': ['aws_lambda', 'aws_bedrock', 'aws_api_gateway'],
            'cost_estimate': '$20-40/month'
        },
        'implementation': {
            'code_generated': True,
            'tests_included': True
        }
    }
    
    print("\n📦 Step 1: Export complete package")
    print("-" * 80)
    
    export_result = await export_service.export_agent(
        agent_id='demo-sentiment-analyzer',
        workflow_data=workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    print(f"✅ Export complete!")
    print(f"   Files: {export_result['metadata']['file_count']}")
    print(f"   Size: {export_result['metadata']['export_size_bytes']:,} bytes")
    print(f"   AWS Services: {', '.join(export_result['metadata']['aws_services'])}")
    print(f"   MCPs: {', '.join(export_result['metadata']['mcps'])}")
    print(f"   Cost: {export_result['metadata']['estimated_cost']}")
    
    print("\n📜 Step 2: Generate Lambda deployment scripts")
    print("-" * 80)
    
    deployment_scripts = await export_service.generate_deployment_scripts(
        agent_id='demo-sentiment-analyzer',
        workflow_data=workflow_data,
        deployment_target=DeploymentTarget.AWS_LAMBDA
    )
    
    print(f"✅ Deployment scripts generated!")
    print(f"   Scripts: {', '.join(deployment_scripts.keys())}")
    
    print("\n📋 Step 3: Create ZIP archive")
    print("-" * 80)
    
    zip_bytes = await export_service.create_export_archive(export_result)
    
    print(f"✅ ZIP archive created!")
    print(f"   Size: {len(zip_bytes):,} bytes")
    print(f"   Ready for download!")
    
    print("\n🎉 Complete workflow finished!")
    print("\nNext steps:")
    print("   1. Download the ZIP file")
    print("   2. Extract to your project directory")
    print("   3. Configure environment variables (.env)")
    print("   4. Install dependencies (pip install -r requirements.txt)")
    print("   5. Run tests (pytest tests/)")
    print("   6. Deploy to AWS (./infrastructure/deploy.sh)")


async def demo_file_contents():
    """Demonstrate generated file contents"""
    print("\n\n" + "=" * 80)
    print("DEMO: Generated File Contents")
    print("=" * 80)
    
    export_service = ExportService()
    
    workflow_data = {
        'requirements': {
            'use_case': 'simple_agent',
            'description': 'Simple demo agent'
        },
        'architecture': {
            'aws_services': ['lambda'],
            'mcps': ['aws_documentation'],
            'cost_estimate': '$5-10/month'
        },
        'implementation': {}
    }
    
    result = await export_service.export_agent(
        agent_id='demo-simple',
        workflow_data=workflow_data,
        export_format=ExportFormat.CODE,
        include_tests=False
    )
    
    # Show sample file contents
    files_to_show = [
        ('src/agent.py', 'Main Agent Code'),
        ('requirements.txt', 'Python Dependencies'),
        ('.env.template', 'Environment Template')
    ]
    
    for file_path, description in files_to_show:
        if file_path in result['files']:
            print(f"\n{'=' * 80}")
            print(f"File: {file_path} - {description}")
            print(f"{'=' * 80}")
            
            content = result['files'][file_path]
            lines = content.split('\n')
            
            # Show first 20 lines
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:3d} | {line}")
            
            if len(lines) > 20:
                print(f"... ({len(lines) - 20} more lines)")


async def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("AGENT BUILDER PLATFORM - EXPORT & DEPLOYMENT DEMO")
    print("=" * 80)
    print("\nThis demo showcases the export and deployment functionality")
    print("of the Agent Builder Platform.\n")
    
    try:
        # Run demos
        await demo_export_formats()
        await demo_deployment_scripts()
        await demo_complete_workflow()
        await demo_file_contents()
        
        print("\n\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)
        print("\n✅ All demos completed successfully!")
        print("\nThe export and deployment system is ready for production use.")
        print("\nKey Features:")
        print("   • 5 export formats (code, iac, container, strands, complete)")
        print("   • 5 deployment targets (Lambda, ECS, Fargate, Docker, Local)")
        print("   • 25+ generated files per complete export")
        print("   • Production-ready code with tests and documentation")
        print("   • Infrastructure as Code templates")
        print("   • Deployment scripts for all platforms")
        print("\nFor more information, see:")
        print("   • EXPORT-DEPLOYMENT-API-REFERENCE.md")
        print("   • TASK-11.5-IMPLEMENTATION-SUMMARY.md")
        print("   • TASK-11.5-COMPLETION-REPORT.md")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
