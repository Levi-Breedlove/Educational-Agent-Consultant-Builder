# AWS Architecture Diagram Generation Standards

## Overview

This document defines the mandatory standards for generating AWS architecture diagrams. All AI agents, backend services, and diagram generation code MUST follow these specifications to ensure consistent, professional, and collision-free diagrams.

## Critical Spacing Requirements

### Icon Dimensions
- **Icon height**: 110px (70px icon + 40px label space)
- **Icon width**: 90px
- **Total footprint**: 90px × 110px per service node

### Minimum Vertical Spacing
- **Minimum gap between rows**: 140px
- **Calculation**: 110px (icon height) + 30px (clearance) = 140px
- **Standard y-coordinates**: 60, 200, 340, 480, 620, 760...
- **Formula**: `y = 60 + (row_index * 140)` where row_index starts at 0

### Minimum Horizontal Spacing
- **Minimum gap between columns**: 150px
- **Calculation**: 90px (icon width) + 60px (clearance) = 150px
- **Standard x-coordinates**: 50, 200, 350, 500, 650, 800...
- **Formula**: `x = 50 + (col_index * 150)` where col_index starts at 0

## Service Node Structure

### TypeScript Interface
```typescript
interface ServiceNode {
  id: string              // Unique identifier (e.g., 'lambda1', 'dynamodb')
  name: string            // Display name (e.g., 'AWS Lambda', 'Amazon DynamoDB')
  type: 'aws' | 'generic' // Service type
  icon: React.ComponentType // AWS icon component
  description: string     // Brief description for tooltip
  x: number              // X-coordinate (must follow spacing rules)
  y: number              // Y-coordinate (must follow spacing rules)
}
```

### Example Service Nodes
```typescript
// CORRECT - Proper spacing (140px vertical gaps)
const services = [
  { id: 'apigw', name: 'Amazon API Gateway', type: 'aws', icon: ApiGatewayIcon, 
    description: 'REST API', x: 50, y: 200 },
  { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, 
    description: 'Business logic', x: 200, y: 200 },
  { id: 'dynamodb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, 
    description: 'Database', x: 350, y: 60 },   // 140px above row 2
  { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, 
    description: 'Storage', x: 350, y: 340 },   // 140px below row 2
]

// INCORRECT - Icons will overlap
const badServices = [
  { id: 'service1', x: 50, y: 100 },
  { id: 'service2', x: 50, y: 150 },  // ❌ Only 50px gap - WILL OVERLAP!
]
```

## Connection Structure

### TypeScript Interface
```typescript
interface Connection {
  from: string           // Source service ID
  to: string            // Target service ID
  label?: string        // Optional connection label
  dashed?: boolean      // Optional dashed line style
}
```

### Label Collision Avoidance
The diagram component automatically handles label positioning with:
- **4 fallback positions**: above, below, left, right of connection midpoint
- **20px safety margin** around all icons
- **Automatic collision detection** algorithm

## Layout Patterns

### Single Row Layout
```typescript
// Horizontal services at same y-coordinate
const singleRow = [
  { id: 'client', x: 50, y: 200 },
  { id: 'apigw', x: 200, y: 200 },
  { id: 'lambda', x: 350, y: 200 },
  { id: 'database', x: 500, y: 200 },
]
```

### Multi-Row Layout (Recommended)
```typescript
// Services distributed across rows with 140px gaps
const multiRow = [
  // Row 1 (y=60)
  { id: 'iam', x: 200, y: 60 },
  { id: 'secrets', x: 350, y: 60 },
  
  // Row 2 (y=200) - Main flow
  { id: 'client', x: 50, y: 200 },
  { id: 'apigw', x: 200, y: 200 },
  { id: 'lambda', x: 350, y: 200 },
  
  // Row 3 (y=340)
  { id: 's3', x: 200, y: 340 },
  { id: 'cloudwatch', x: 350, y: 340 },
]
```

### Layered Architecture Pattern
```typescript
// Typical 3-tier architecture
const layered = [
  // Presentation Layer (y=60)
  { id: 'cloudfront', x: 200, y: 60 },
  { id: 'waf', x: 350, y: 60 },
  
  // Application Layer (y=200)
  { id: 'alb', x: 50, y: 200 },
  { id: 'ecs', x: 200, y: 200 },
  { id: 'lambda', x: 350, y: 200 },
  
  // Data Layer (y=340)
  { id: 'rds', x: 200, y: 340 },
  { id: 'dynamodb', x: 350, y: 340 },
  { id: 's3', x: 500, y: 340 },
  
  // Monitoring Layer (y=480)
  { id: 'cloudwatch', x: 200, y: 480 },
  { id: 'xray', x: 350, y: 480 },
]
```

## AI Agent Instructions

### For Architecture Advisor Agent

When generating architecture diagrams, you MUST:

1. **Calculate positions using the spacing formulas**:
   ```python
   def calculate_position(row: int, col: int) -> tuple[int, int]:
       x = 50 + (col * 150)  # 150px horizontal spacing
       y = 60 + (row * 140)  # 140px vertical spacing
       return (x, y)
   ```

2. **Validate spacing before returning**:
   ```python
   def validate_spacing(services: list) -> bool:
       for i, service1 in enumerate(services):
           for service2 in services[i+1:]:
               dx = abs(service1['x'] - service2['x'])
               dy = abs(service1['y'] - service2['y'])
               
               # Check vertical spacing
               if dx < 90 and dy < 140:
                   return False  # Vertical overlap!
               
               # Check horizontal spacing  
               if dy < 110 and dx < 150:
                   return False  # Horizontal overlap!
       
       return True
   ```

3. **Use standard y-coordinates**: 60, 200, 340, 480, 620, 760
4. **Use standard x-coordinates**: 50, 200, 350, 500, 650, 800

### Example Agent Output Format

```json
{
  "architecture": {
    "services": [
      {
        "id": "apigw",
        "name": "Amazon API Gateway",
        "type": "aws",
        "icon": "ApiGatewayIcon",
        "description": "REST API endpoint",
        "x": 50,
        "y": 200
      },
      {
        "id": "lambda",
        "name": "AWS Lambda",
        "type": "aws",
        "icon": "LambdaIcon",
        "description": "Business logic",
        "x": 200,
        "y": 200
      },
      {
        "id": "dynamodb",
        "name": "Amazon DynamoDB",
        "type": "aws",
        "icon": "DynamoDbIcon",
        "description": "NoSQL database",
        "x": 350,
        "y": 60
      }
    ],
    "connections": [
      { "from": "apigw", "to": "lambda", "label": "invoke" },
      { "from": "lambda", "to": "dynamodb", "label": "read/write" }
    ]
  }
}
```

## Backend API Requirements

### Diagram Generation Endpoint

The backend MUST validate all generated diagrams:

```python
from typing import List, Dict

class DiagramValidator:
    ICON_WIDTH = 90
    ICON_HEIGHT = 110
    MIN_HORIZONTAL_GAP = 150
    MIN_VERTICAL_GAP = 140
    
    @staticmethod
    def validate_diagram(services: List[Dict]) -> tuple[bool, List[str]]:
        """
        Validates diagram spacing and returns (is_valid, errors)
        """
        errors = []
        
        for i, s1 in enumerate(services):
            for s2 in services[i+1:]:
                dx = abs(s1['x'] - s2['x'])
                dy = abs(s1['y'] - s2['y'])
                
                # Check for overlaps
                if dx < DiagramValidator.ICON_WIDTH and dy < DiagramValidator.MIN_VERTICAL_GAP:
                    errors.append(
                        f"Vertical overlap between {s1['id']} and {s2['id']}: "
                        f"gap={dy}px, required={DiagramValidator.MIN_VERTICAL_GAP}px"
                    )
                
                if dy < DiagramValidator.ICON_HEIGHT and dx < DiagramValidator.MIN_HORIZONTAL_GAP:
                    errors.append(
                        f"Horizontal overlap between {s1['id']} and {s2['id']}: "
                        f"gap={dx}px, required={DiagramValidator.MIN_HORIZONTAL_GAP}px"
                    )
        
        return (len(errors) == 0, errors)
    
    @staticmethod
    def auto_fix_spacing(services: List[Dict]) -> List[Dict]:
        """
        Automatically adjusts positions to meet spacing requirements
        """
        # Group services by approximate row
        rows = {}
        for service in services:
            row_key = round(service['y'] / 140)
            if row_key not in rows:
                rows[row_key] = []
            rows[row_key].append(service)
        
        # Adjust to standard positions
        fixed_services = []
        for row_idx, row_services in sorted(rows.items()):
            y = 60 + (row_idx * 140)
            
            # Sort by x position
            row_services.sort(key=lambda s: s['x'])
            
            for col_idx, service in enumerate(row_services):
                x = 50 + (col_idx * 150)
                fixed_services.append({
                    **service,
                    'x': x,
                    'y': y
                })
        
        return fixed_services
```

## Available AWS Icons

### Compute Services
- `ApiGatewayIcon` - Amazon API Gateway
- `LambdaIcon` - AWS Lambda
- `EcsIcon` - Amazon ECS Fargate
- `EC2Icon` - Amazon EC2

### Storage Services
- `S3Icon` - Amazon S3
- `DynamoDbIcon` - Amazon DynamoDB
- `RdsIcon` - Amazon RDS
- `ElastiCacheIcon` - Amazon ElastiCache
- `RedshiftIcon` - Amazon Redshift

### Networking Services
- `AlbIcon` - Elastic Load Balancing
- `CloudFrontIcon` - Amazon CloudFront
- `Route53Icon` - Amazon Route 53
- `VpcIcon` - Amazon VPC

### AI/ML Services
- `BedrockIcon` - Amazon Bedrock
- `SageMakerIcon` - Amazon SageMaker
- `LexIcon` - Amazon Lex

### Analytics Services
- `KinesisIcon` - Amazon Kinesis
- `GlueIcon` - AWS Glue
- `AthenaIcon` - Amazon Athena
- `QuickSightIcon` - Amazon QuickSight
- `EMRIcon` - Amazon EMR
- `OpenSearchServiceIcon` - Amazon OpenSearch Service

### Integration Services
- `EventBridgeIcon` - Amazon EventBridge
- `SqsIcon` - Amazon SQS
- `SnsIcon` - Amazon SNS
- `StepFunctionsIcon` - AWS Step Functions

### Security Services
- `IamIcon` - AWS IAM
- `CognitoIcon` - Amazon Cognito
- `WAFIcon` - AWS WAF
- `SecretsManagerIcon` - AWS Secrets Manager

### Monitoring Services
- `CloudWatchIcon` - Amazon CloudWatch

### Developer Tools
- `CodePipelineIcon` - AWS CodePipeline
- `CodeBuildIcon` - AWS CodeBuild
- `CodeDeployIcon` - AWS CodeDeploy

### Generic Icons
- `UserIcon` - End User
- `ClientIcon` - Client Application

## Testing & Validation

### Manual Testing Checklist
- [ ] All icons are visible and not overlapping
- [ ] Minimum 140px vertical spacing between rows
- [ ] Minimum 150px horizontal spacing between columns
- [ ] Connection labels are readable and not overlapping icons
- [ ] Diagram fits within viewport (max width ~900px recommended)
- [ ] All service names are displayed correctly

### Automated Validation
```typescript
// Frontend validation utility
export function validateDiagramSpacing(services: ServiceNode[]): {
  valid: boolean
  errors: string[]
} {
  const errors: string[] = []
  const MIN_VERTICAL_GAP = 140
  const MIN_HORIZONTAL_GAP = 150
  const ICON_WIDTH = 90
  const ICON_HEIGHT = 110
  
  for (let i = 0; i < services.length; i++) {
    for (let j = i + 1; j < services.length; j++) {
      const s1 = services[i]
      const s2 = services[j]
      const dx = Math.abs(s1.x - s2.x)
      const dy = Math.abs(s1.y - s2.y)
      
      if (dx < ICON_WIDTH && dy < MIN_VERTICAL_GAP) {
        errors.push(`Vertical overlap: ${s1.id} and ${s2.id}`)
      }
      
      if (dy < ICON_HEIGHT && dx < MIN_HORIZONTAL_GAP) {
        errors.push(`Horizontal overlap: ${s1.id} and ${s2.id}`)
      }
    }
  }
  
  return { valid: errors.length === 0, errors }
}
```

## Common Mistakes to Avoid

### ❌ WRONG - Insufficient Spacing
```typescript
// Icons will overlap!
const bad = [
  { id: 'service1', x: 100, y: 100 },
  { id: 'service2', x: 100, y: 150 },  // Only 50px gap
  { id: 'service3', x: 100, y: 200 },  // Only 50px gap
]
```

### ✅ CORRECT - Proper Spacing
```typescript
// Perfect spacing
const good = [
  { id: 'service1', x: 100, y: 60 },
  { id: 'service2', x: 100, y: 200 },   // 140px gap
  { id: 'service3', x: 100, y: 340 },   // 140px gap
]
```

### ❌ WRONG - Random Coordinates
```typescript
// Inconsistent and hard to maintain
const bad = [
  { id: 'service1', x: 73, y: 127 },
  { id: 'service2', x: 234, y: 189 },
]
```

### ✅ CORRECT - Standard Grid
```typescript
// Clean, consistent grid
const good = [
  { id: 'service1', x: 50, y: 60 },
  { id: 'service2', x: 200, y: 200 },
]
```

## Summary

**Key Rules:**
1. ✅ Use standard y-coordinates: 60, 200, 340, 480, 620...
2. ✅ Use standard x-coordinates: 50, 200, 350, 500, 650...
3. ✅ Minimum 140px vertical spacing between rows
4. ✅ Minimum 150px horizontal spacing between columns
5. ✅ Validate all diagrams before rendering
6. ✅ Use auto-fix function if spacing violations detected

**Zero Tolerance:**
- ❌ No overlapping icons
- ❌ No spacing violations
- ❌ No random coordinates

**Result:**
- 🎯 Professional, clean diagrams
- 🎯 Consistent visual language
- 🎯 Zero collision issues
- 🎯 Production-ready quality

---

**Document Version**: 1.0  
**Last Updated**: October 8, 2025  
**Status**: MANDATORY FOR ALL DIAGRAM GENERATION
