#!/usr/bin/env python3
"""
Expand AWS Service Icon Registry
Adds 150 more commonly-used AWS services to the icon registry
"""

import os
import re

# Path to the icon library
ICONS_PATH = "node_modules/aws-react-icons/lib/icons"

# Services to add (150 additional commonly-used services)
ADDITIONAL_SERVICES = {
    # COMPUTE (10 more)
    'ArchitectureServiceAWSOutposts': ('AWS Outposts', 'Compute', 'Run AWS infrastructure on-premises'),
    'ArchitectureServiceAWSWavelength': ('AWS Wavelength', 'Compute', '5G edge computing'),
    'ArchitectureServiceAWSLocalZones': ('AWS Local Zones', 'Compute', 'Low-latency compute closer to users'),
    'ArchitectureServiceAWSServerlessApplicationRepository': ('AWS Serverless Application Repository', 'Compute', 'Discover and deploy serverless applications'),
    'ArchitectureServiceAWSServerlessApplicationModel': ('AWS SAM', 'Compute', 'Build serverless applications'),
    'ArchitectureServiceVMwareCloudOnAWS': ('VMware Cloud on AWS', 'Compute', 'Migrate VMware workloads'),
    'ArchitectureServiceAWSParallelCluster': ('AWS ParallelCluster', 'Compute', 'HPC cluster management'),
    'ArchitectureServiceAWSNitroEnclaves': ('AWS Nitro Enclaves', 'Compute', 'Isolated compute environments'),
    'ArchitectureServiceAWSApp2Container': ('AWS App2Container', 'Compute', 'Containerize applications'),
    'ArchitectureServiceAmazonECRPublic': ('Amazon ECR Public', 'Compute', 'Public container registry'),
    
    # STORAGE (8 more)
    'ArchitectureServiceAmazonS3Glacier': ('Amazon S3 Glacier', 'Storage', 'Long-term archive storage'),
    'ArchitectureServiceAmazonS3GlacierDeepArchive': ('S3 Glacier Deep Archive', 'Storage', 'Lowest-cost archive storage'),
    'ArchitectureServiceAWSSnowballEdge': ('AWS Snowball Edge', 'Storage', 'Edge computing and data transfer'),
    'ArchitectureServiceAWSSnowcone': ('AWS Snowcone', 'Storage', 'Small edge computing device'),
    'ArchitectureServiceAWSSnowmobile': ('AWS Snowmobile', 'Storage', 'Exabyte-scale data transfer'),
    'ArchitectureServiceAmazonFileCache': ('Amazon File Cache', 'Storage', 'High-speed cache for file data'),
    'ArchitectureServiceAWSElasticDisasterRecovery': ('AWS Elastic Disaster Recovery', 'Storage', 'Application recovery service'),
    'ArchitectureServiceAWSBackupGateway': ('AWS Backup Gateway', 'Storage', 'Backup on-premises to AWS'),
    
    # DATABASE (10 more)
    'ArchitectureServiceAmazonQLDB': ('Amazon QLDB', 'Database', 'Ledger database'),
    'ArchitectureServiceAmazonDynamoDBAccelerator': ('DynamoDB Accelerator (DAX)', 'Database', 'In-memory cache for DynamoDB'),
    'ArchitectureServiceAmazonRDSProxy': ('Amazon RDS Proxy', 'Database', 'Managed database proxy'),
    'ArchitectureServiceAmazonRDSonVMware': ('Amazon RDS on VMware', 'Database', 'Managed databases on-premises'),
    'ArchitectureServiceAmazonAuroraServerless': ('Amazon Aurora Serverless', 'Database', 'On-demand autoscaling database'),
    'ArchitectureServiceAWSDatabase MigrationService': ('AWS DMS', 'Database', 'Database migration service'),
    'ArchitectureServiceAWSSchemaConversionTool': ('AWS SCT', 'Database', 'Convert database schemas'),
    'ArchitectureServiceAmazonElastiCacheforRedis': ('ElastiCache for Redis', 'Database', 'Redis-compatible cache'),
    'ArchitectureServiceAmazonElastiCacheforMemcached': ('ElastiCache for Memcached', 'Database', 'Memcached-compatible cache'),
    'ArchitectureServiceAmazonMemoryDBforRedis': ('MemoryDB for Redis', 'Database', 'Redis-compatible durable database'),
    
    # NETWORKING (15 more)
    'ArchitectureServiceAWSPrivateLink': ('AWS PrivateLink', 'Networking', 'Private connectivity to services'),
    'ArchitectureServiceAWSVPN': ('AWS VPN', 'Networking', 'Secure network connections'),
    'ArchitectureServiceAWSClientVPN': ('AWS Client VPN', 'Networking', 'Managed client-based VPN'),
    'ArchitectureServiceAWSSitetoSiteVPN': ('AWS Site-to-Site VPN', 'Networking', 'Connect networks to AWS'),
    'ArchitectureServiceAWSNetworkFirewall': ('AWS Network Firewall', 'Networking', 'Network protection'),
    'ArchitectureServiceAWSVerifiedAccess': ('AWS Verified Access', 'Networking', 'Secure application access'),
    'ArchitectureServiceAmazonVPCLattice': ('Amazon VPC Lattice', 'Networking', 'Service-to-service connectivity'),
    'ArchitectureServiceElasticLoadBalancingApplicationLoadBalancer': ('Application Load Balancer', 'Networking', 'Layer 7 load balancing'),
    'ArchitectureServiceElasticLoadBalancingNetworkLoadBalancer': ('Network Load Balancer', 'Networking', 'Layer 4 load balancing'),
    'ArchitectureServiceElasticLoadBalancingGatewayLoadBalancer': ('Gateway Load Balancer', 'Networking', 'Third-party appliances'),
    'ArchitectureServiceAmazonRoute53Resolver': ('Route 53 Resolver', 'Networking', 'DNS resolution for hybrid clouds'),
    'ArchitectureServiceAmazonRoute53ApplicationRecoveryController': ('Route 53 ARC', 'Networking', 'Application recovery readiness'),
    'ArchitectureServiceAWSCloudWAN': ('AWS Cloud WAN', 'Networking', 'Build and manage global networks'),
    'ArchitectureServiceAWSPrivate5G': ('AWS Private 5G', 'Networking', 'Private mobile network'),
    'ArchitectureServiceAmazonAPIGatewayWebSocketAPI': ('API Gateway WebSocket', 'Networking', 'Real-time two-way communication'),
    
    # SECURITY (15 more)
    'ArchitectureServiceAWSDirectoryService': ('AWS Directory Service', 'Security', 'Managed Active Directory'),
    'ArchitectureServiceAWSResourceAccessManager': ('AWS RAM', 'Security', 'Share AWS resources'),
    'ArchitectureServiceAWSAuditManager': ('AWS Audit Manager', 'Security', 'Audit AWS usage'),
    'ArchitectureServiceAWSArtifact': ('AWS Artifact', 'Security', 'Compliance reports'),
    'ArchitectureServiceAmazonDetective': ('Amazon Detective', 'Security', 'Security investigation'),
    'ArchitectureServiceAWSSecurityLake': ('AWS Security Lake', 'Security', 'Centralize security data'),
    'ArchitectureServiceAWSFirewallManager': ('AWS Firewall Manager', 'Security', 'Central firewall management'),
    'ArchitectureServiceAWSNetworkFirewall': ('AWS Network Firewall', 'Security', 'Network protection'),
    'ArchitectureServiceAWSSigner': ('AWS Signer', 'Security', 'Code signing'),
    'ArchitectureServiceAWSPrivateCertificateAuthority': ('AWS Private CA', 'Security', 'Private certificate authority'),
    'ArchitectureServiceAWSPaymentCryptography': ('AWS Payment Cryptography', 'Security', 'Payment HSM'),
    'ArchitectureServiceAmazonVerifiedPermissions': ('Amazon Verified Permissions', 'Security', 'Fine-grained authorization'),
    'ArchitectureServiceAWSIAMIdentityCenter': ('AWS IAM Identity Center', 'Security', 'Workforce identity management'),
    'ArchitectureServiceAmazonSecurityLake': ('Amazon Security Lake', 'Security', 'Security data lake'),
    'ArchitectureServiceAWSCloudHSMClassic': ('AWS CloudHSM Classic', 'Security', 'Hardware security module'),
    
    # MACHINE LEARNING (12 more)
    'ArchitectureServiceAmazonAugmentedAI': ('Amazon Augmented AI', 'Machine Learning', 'Human review of ML predictions'),
    'ArchitectureServiceAmazonCodeGuru': ('Amazon CodeGuru', 'Machine Learning', 'Automated code reviews'),
    'ArchitectureServiceAmazonCodeWhisperer': ('Amazon CodeWhisperer', 'Machine Learning', 'AI code companion'),
    'ArchitectureServiceAmazonDevOpsGuru': ('Amazon DevOps Guru', 'Machine Learning', 'ML-powered operations'),
    'ArchitectureServiceAmazonFraudDetector': ('Amazon Fraud Detector', 'Machine Learning', 'Fraud detection service'),
    'ArchitectureServiceAmazonHealthLake': ('Amazon HealthLake', 'Machine Learning', 'Healthcare data store'),
    'ArchitectureServiceAmazonLookoutforEquipment': ('Amazon Lookout for Equipment', 'Machine Learning', 'Detect abnormal equipment behavior'),
    'ArchitectureServiceAmazonLookoutforMetrics': ('Amazon Lookout for Metrics', 'Machine Learning', 'Detect anomalies in metrics'),
    'ArchitectureServiceAmazonLookoutforVision': ('Amazon Lookout for Vision', 'Machine Learning', 'Spot product defects'),
    'ArchitectureServiceAmazonMonitron': ('Amazon Monitron', 'Machine Learning', 'Equipment monitoring'),
    'ArchitectureServiceAWSPanorama': ('AWS Panorama', 'Machine Learning', 'Computer vision at the edge'),
    'ArchitectureServiceAmazonSageMakerGroundTruth': ('SageMaker Ground Truth', 'Machine Learning', 'Data labeling'),
    
    # ANALYTICS (12 more)
    'ArchitectureServiceAmazonCloudSearch': ('Amazon CloudSearch', 'Analytics', 'Managed search service'),
    'ArchitectureServiceAmazonDataZone': ('Amazon DataZone', 'Analytics', 'Data governance'),
    'ArchitectureServiceAmazonFinSpace': ('Amazon FinSpace', 'Analytics', 'Financial services data management'),
    'ArchitectureServiceAWSDataExchange': ('AWS Data Exchange', 'Analytics', 'Find and subscribe to data'),
    'ArchitectureServiceAWSDataPipeline': ('AWS Data Pipeline', 'Analytics', 'Orchestrate data workflows'),
    'ArchitectureServiceAmazonKinesisDataStreams': ('Kinesis Data Streams', 'Analytics', 'Real-time data streaming'),
    'ArchitectureServiceAmazonKinesisDataFirehose': ('Kinesis Data Firehose', 'Analytics', 'Load streaming data'),
    'ArchitectureServiceAmazonKinesisDataAnalytics': ('Kinesis Data Analytics', 'Analytics', 'Analyze streaming data'),
    'ArchitectureServiceAmazonKinesisVideoStreams': ('Kinesis Video Streams', 'Analytics', 'Process video streams'),
    'ArchitectureServiceAmazonManagedServiceforApacheFlink': ('Managed Service for Apache Flink', 'Analytics', 'Stream processing'),
    'ArchitectureServiceAmazonRedshiftServerless': ('Redshift Serverless', 'Analytics', 'Serverless data warehouse'),
    'ArchitectureServiceAWSCleanRooms': ('AWS Clean Rooms', 'Analytics', 'Collaborate on datasets'),
    
    # APPLICATION INTEGRATION (8 more)
    'ArchitectureServiceAmazonManagedWorkflowsforApacheAirflow': ('Amazon MWAA', 'Application Integration', 'Managed Apache Airflow'),
    'ArchitectureServiceAWSExpressWorkflows': ('AWS Express Workflows', 'Application Integration', 'High-volume workflows'),
    'ArchitectureServiceAmazonSimpleWorkflowService': ('Amazon SWF', 'Application Integration', 'Workflow service'),
    'ArchitectureServiceAmazonAppFlowforSalesforce': ('AppFlow for Salesforce', 'Application Integration', 'Salesforce integration'),
    'ArchitectureServiceAWSFaultInjectionSimulator': ('AWS FIS', 'Application Integration', 'Chaos engineering'),
    'ArchitectureServiceAmazonEventBridgePipes': ('EventBridge Pipes', 'Application Integration', 'Point-to-point integrations'),
    'ArchitectureServiceAmazonEventBridgeScheduler': ('EventBridge Scheduler', 'Application Integration', 'Scheduled tasks'),
    'ArchitectureServiceAWSAppFabric': ('AWS AppFabric', 'Application Integration', 'SaaS application connectivity'),
    
    # MANAGEMENT & GOVERNANCE (15 more)
    'ArchitectureServiceAWSLicenseManager': ('AWS License Manager', 'Management', 'Manage software licenses'),
    'ArchitectureServiceAWSManagedServices': ('AWS Managed Services', 'Management', 'Infrastructure operations'),
    'ArchitectureServiceAWSProton': ('AWS Proton', 'Management', 'Automated infrastructure provisioning'),
    'ArchitectureServiceAWSServiceManagementConnector': ('AWS Service Management Connector', 'Management', 'ITSM integration'),
    'ArchitectureServiceAWSChatbot': ('AWS Chatbot', 'Management', 'ChatOps for AWS'),
    'ArchitectureServiceAWSLaunchWizard': ('AWS Launch Wizard', 'Management', 'Deploy applications easily'),
    'ArchitectureServiceAWSOpsWorks': ('AWS OpsWorks', 'Management', 'Configuration management'),
    'ArchitectureServiceAWSOpsWorksforChef': ('OpsWorks for Chef', 'Management', 'Managed Chef'),
    'ArchitectureServiceAWSOpsWorksforPuppet': ('OpsWorks for Puppet', 'Management', 'Managed Puppet'),
    'ArchitectureServiceAWSPersonalHealthDashboard': ('AWS Personal Health Dashboard', 'Management', 'Personalized service health'),
    'ArchitectureServiceAWSResilientHub': ('AWS Resilience Hub', 'Management', 'Application resilience'),
    'ArchitectureServiceAWSResourceGroups': ('AWS Resource Groups', 'Management', 'Organize AWS resources'),
    'ArchitectureServiceAWSSystemsManagerAppConfig': ('Systems Manager AppConfig', 'Management', 'Application configuration'),
    'ArchitectureServiceAWSSystemsManagerParameterStore': ('Systems Manager Parameter Store', 'Management', 'Secure parameter storage'),
    'ArchitectureServiceAmazonCloudWatchLogs': ('CloudWatch Logs', 'Management', 'Log monitoring'),
    
    # DEVELOPER TOOLS (10 more)
    'ArchitectureServiceAWSCodeArtifact': ('AWS CodeArtifact', 'Developer Tools', 'Artifact repository'),
    'ArchitectureServiceAWSCodeStar': ('AWS CodeStar', 'Developer Tools', 'Develop and deploy applications'),
    'ArchitectureServiceAWSCodeStarConnections': ('CodeStar Connections', 'Developer Tools', 'Connect to source providers'),
    'ArchitectureServiceAWSFaultInjectionSimulator': ('AWS FIS', 'Developer Tools', 'Chaos engineering'),
    'ArchitectureServiceAmazonCodeCatalyst': ('Amazon CodeCatalyst', 'Developer Tools', 'Unified software development'),
    'ArchitectureServiceAWSApplicationComposer': ('AWS Application Composer', 'Developer Tools', 'Visual serverless design'),
    'ArchitectureServiceAWSCloudControlAPI': ('AWS Cloud Control API', 'Developer Tools', 'Manage AWS resources'),
    'ArchitectureServiceAWSCloudDevelopmentKit': ('AWS CDK', 'Developer Tools', 'Infrastructure as code'),
    'ArchitectureServiceAWSToolsandSDKs': ('AWS Tools and SDKs', 'Developer Tools', 'Developer tools'),
    'ArchitectureServiceAWSXRayInsights': ('X-Ray Insights', 'Developer Tools', 'Application insights'),
    
    # MIGRATION & TRANSFER (8 more)
    'ArchitectureServiceAWSMainframeModernization': ('AWS Mainframe Modernization', 'Migration', 'Modernize mainframe applications'),
    'ArchitectureServiceAWSMigrationEvaluator': ('AWS Migration Evaluator', 'Migration', 'Build migration business case'),
    'ArchitectureServiceAWSApplicationDiscoveryService': ('AWS Application Discovery', 'Migration', 'Discover on-premises applications'),
    'ArchitectureServiceAWSServerMigrationService': ('AWS SMS', 'Migration', 'Migrate on-premises servers'),
    'ArchitectureServiceAWSTransferforSFTP': ('AWS Transfer for SFTP', 'Migration', 'SFTP file transfers'),
    'ArchitectureServiceAWSTransferforFTPS': ('AWS Transfer for FTPS', 'Migration', 'FTPS file transfers'),
    'ArchitectureServiceAWSTransferforFTP': ('AWS Transfer for FTP', 'Migration', 'FTP file transfers'),
    'ArchitectureServiceAWSDataSyncDiscovery': ('DataSync Discovery', 'Migration', 'Discover storage for migration'),
    
    # FRONT-END WEB & MOBILE (5 more)
    'ArchitectureServiceAWSAmplifyStudio': ('AWS Amplify Studio', 'Front-End', 'Visual development'),
    'ArchitectureServiceAWSAmplifyHosting': ('Amplify Hosting', 'Front-End', 'Host web apps'),
    'ArchitectureServiceAmazonLocationService': ('Amazon Location Service', 'Front-End', 'Add location data'),
    'ArchitectureServiceAmazonPinpoint': ('Amazon Pinpoint', 'Front-End', 'Customer engagement'),
    'ArchitectureServiceAmazonSimpleEmailService': ('Amazon SES', 'Front-End', 'Email sending service'),
    
    # MEDIA SERVICES (8 more)
    'ArchitectureServiceAWSElementalMediaTailor': ('AWS Elemental MediaTailor', 'Media', 'Video monetization'),
    'ArchitectureServiceAWSElementalMediaConnect': ('AWS Elemental MediaConnect', 'Media', 'Live video transport'),
    'ArchitectureServiceAmazonInteractiveVideoService': ('Amazon IVS', 'Media', 'Live streaming'),
    'ArchitectureServiceAmazonKinesisVideoStreamsWebRTC': ('Kinesis Video Streams WebRTC', 'Media', 'Real-time video'),
    'ArchitectureServiceAmazonNimbleStudio': ('Amazon Nimble Studio', 'Media', 'Creative studio in the cloud'),
    'ArchitectureServiceAWSThinkboxDeadline': ('AWS Thinkbox Deadline', 'Media', 'Render farm management'),
    'ArchitectureServiceAWSThinkboxKrakatoa': ('AWS Thinkbox Krakatoa', 'Media', 'Volumetric rendering'),
    'ArchitectureServiceAWSThinkboxSequoia': ('AWS Thinkbox Sequoia', 'Media', 'Point cloud rendering'),
    
    # IOT (8 more)
    'ArchitectureServiceAWSIoTSiteWise': ('AWS IoT SiteWise', 'IoT', 'Industrial data collection'),
    'ArchitectureServiceAWSIoTTwinMaker': ('AWS IoT TwinMaker', 'IoT', 'Digital twins'),
    'ArchitectureServiceAWSIoTFleetWise': ('AWS IoT FleetWise', 'IoT', 'Vehicle data collection'),
    'ArchitectureServiceAWSIoTRoboRunner': ('AWS IoT RoboRunner', 'IoT', 'Robot fleet management'),
    'ArchitectureServiceAWSIoTDeviceManagement': ('AWS IoT Device Management', 'IoT', 'Manage IoT devices'),
    'ArchitectureServiceAWSIoTDeviceDefender': ('AWS IoT Device Defender', 'IoT', 'IoT security'),
    'ArchitectureServiceAWSIoT1Click': ('AWS IoT 1-Click', 'IoT', 'Simple device triggers'),
    'ArchitectureServiceAWSIoTButton': ('AWS IoT Button', 'IoT', 'Programmable button'),
    
    # BUSINESS APPLICATIONS (10 more)
    'ArchitectureServiceAmazonConnect': ('Amazon Connect', 'Business Applications', 'Cloud contact center'),
    'ArchitectureServiceAmazonConnectCustomerProfiles': ('Connect Customer Profiles', 'Business Applications', 'Unified customer profiles'),
    'ArchitectureServiceAmazonConnectWisdom': ('Connect Wisdom', 'Business Applications', 'Agent knowledge'),
    'ArchitectureServiceAmazonHoneycode': ('Amazon Honeycode', 'Business Applications', 'Build apps without code'),
    'ArchitectureServiceAmazonChime': ('Amazon Chime', 'Business Applications', 'Communications service'),
    'ArchitectureServiceAmazonChimeSDK': ('Amazon Chime SDK', 'Business Applications', 'Real-time communications'),
    'ArchitectureServiceAmazonWorkMail': ('Amazon WorkMail', 'Business Applications', 'Secure email'),
    'ArchitectureServiceAmazonWorkDocs': ('Amazon WorkDocs', 'Business Applications', 'Secure document storage'),
    'ArchitectureServiceAlexaforBusiness': ('Alexa for Business', 'Business Applications', 'Voice-enable organization'),
    'ArchitectureServiceAmazonSimpleEmailServiceSES': ('Amazon SES', 'Business Applications', 'Email service'),
    
    # END USER COMPUTING (6 more)
    'ArchitectureServiceAmazonWorkSpaces': ('Amazon WorkSpaces', 'End User Computing', 'Virtual desktops'),
    'ArchitectureServiceAmazonWorkSpacesWeb': ('WorkSpaces Web', 'End User Computing', 'Secure browser'),
    'ArchitectureServiceAmazonAppStream': ('Amazon AppStream 2.0', 'End User Computing', 'Application streaming'),
    'ArchitectureServiceAmazonWorkSpacesCore': ('WorkSpaces Core', 'End User Computing', 'Virtual desktop infrastructure'),
    'ArchitectureServiceAmazonWorkSpacesThinClient': ('WorkSpaces Thin Client', 'End User Computing', 'Thin client device'),
    'ArchitectureServiceAWSEndUserMessaging': ('AWS End User Messaging', 'End User Computing', 'User messaging'),
}

print(f"Total additional services to add: {len(ADDITIONAL_SERVICES)}")
print("\nGenerating expanded icon registry...")
print("=" * 80)

# Generate the additions
for icon_name, (official_name, category, description) in sorted(ADDITIONAL_SERVICES.items()):
    service_id = icon_name.replace('ArchitectureService', '').replace('AWS', '').replace('Amazon', '').replace('Elastic', '')
    # Convert to kebab-case
    service_id = re.sub(r'([a-z])([A-Z])', r'\1-\2', service_id).lower()
    
    print(f"\n// {official_name}")
    print(f"import {icon_name} from 'aws-react-icons/icons/{icon_name}'")

print("\n\n" + "=" * 80)
print("Registry entries to add:")
print("=" * 80)

for icon_name, (official_name, category, description) in sorted(ADDITIONAL_SERVICES.items()):
    service_id = icon_name.replace('ArchitectureService', '').replace('AWS', '').replace('Amazon', '').replace('Elastic', '')
    service_id = re.sub(r'([a-z])([A-Z])', r'\1-\2', service_id).lower()
    
    # Extract short name
    short_name = official_name.replace('AWS ', '').replace('Amazon ', '').replace('Elastic ', '')
    
    print(f"""
  '{service_id}': {{
    id: '{service_id}',
    name: '{short_name}',
    officialName: '{official_name}',
    icon: {icon_name},
    category: '{category}',
    description: '{description}',
    useCases: [],
    tags: []
  }},""")

print("\n" + "=" * 80)
print(f"✅ Generated {len(ADDITIONAL_SERVICES)} additional service definitions")
print("=" * 80)
