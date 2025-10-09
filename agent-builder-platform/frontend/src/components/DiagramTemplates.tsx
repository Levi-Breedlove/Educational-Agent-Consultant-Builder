import { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Typography,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
} from '@mui/material'
import { Visibility } from '@mui/icons-material'
import ArchitectureVisualizer from './ArchitectureVisualizer'

export interface DiagramTemplate {
  id: string
  name: string
  description: string
  category: string
  diagram: string
  tags: string[]
}

interface DiagramTemplatesProps {
  templates: DiagramTemplate[]
  onSelectTemplate: (template: DiagramTemplate) => void
}

// Common AWS architecture templates
export const defaultTemplates: DiagramTemplate[] = [
  {
    id: 'serverless-api',
    name: 'Serverless API',
    description: 'API Gateway + Lambda + DynamoDB pattern for serverless REST APIs',
    category: 'Serverless',
    tags: ['API', 'Lambda', 'DynamoDB'],
    diagram: `graph TB
    Client[Client] --> APIG[API Gateway]
    APIG --> Lambda[Lambda Function]
    Lambda --> DDB[DynamoDB]
    Lambda --> S3[S3 Bucket]
    CloudWatch[CloudWatch Logs] -.-> Lambda
    IAM[IAM Role] -.-> Lambda`,
  },
  {
    id: 'ecs-fargate',
    name: 'ECS Fargate Application',
    description: 'Containerized application with ECS Fargate, ALB, and RDS',
    category: 'Containers',
    tags: ['ECS', 'Fargate', 'ALB', 'RDS'],
    diagram: `graph TB
    User[User] --> ALB[Application Load Balancer]
    ALB --> ECS[ECS Fargate Service]
    ECS --> RDS[(RDS Database)]
    ECS --> S3[S3 Bucket]
    CloudWatch[CloudWatch] -.-> ECS
    VPC[VPC] -.-> ECS
    VPC -.-> RDS`,
  },
  {
    id: 'event-driven',
    name: 'Event-Driven Architecture',
    description: 'EventBridge + Lambda + SQS for event-driven processing',
    category: 'Event-Driven',
    tags: ['EventBridge', 'Lambda', 'SQS'],
    diagram: `graph TB
    Source[Event Source] --> EB[EventBridge]
    EB --> Lambda1[Lambda Processor]
    EB --> SQS[SQS Queue]
    SQS --> Lambda2[Lambda Consumer]
    Lambda1 --> DDB[DynamoDB]
    Lambda2 --> S3[S3 Bucket]`,
  },
  {
    id: 'ai-agent',
    name: 'AI Agent with Bedrock',
    description: 'Bedrock + Lambda + Knowledge Base for AI agents',
    category: 'AI/ML',
    tags: ['Bedrock', 'Lambda', 'OpenSearch'],
    diagram: `graph TB
    User[User] --> API[API Gateway]
    API --> Lambda[Lambda Orchestrator]
    Lambda --> Bedrock[Amazon Bedrock]
    Lambda --> KB[Knowledge Base]
    KB --> OS[OpenSearch]
    Lambda --> DDB[DynamoDB State]
    S3[S3 Documents] --> KB`,
  },
  {
    id: 'data-pipeline',
    name: 'Data Processing Pipeline',
    description: 'S3 + Lambda + Glue + Athena for data analytics',
    category: 'Analytics',
    tags: ['S3', 'Glue', 'Athena'],
    diagram: `graph TB
    Source[Data Source] --> S3Raw[S3 Raw Data]
    S3Raw --> Lambda[Lambda Trigger]
    Lambda --> Glue[AWS Glue ETL]
    Glue --> S3Processed[S3 Processed Data]
    S3Processed --> Athena[Amazon Athena]
    Athena --> QuickSight[QuickSight Dashboard]`,
  },
  {
    id: 'microservices',
    name: 'Microservices Architecture',
    description: 'API Gateway + Multiple Lambda functions + DynamoDB',
    category: 'Microservices',
    tags: ['API Gateway', 'Lambda', 'DynamoDB'],
    diagram: `graph TB
    Client[Client] --> APIG[API Gateway]
    APIG --> Auth[Auth Service]
    APIG --> Users[User Service]
    APIG --> Orders[Order Service]
    Auth --> DDB1[(Auth DB)]
    Users --> DDB2[(User DB)]
    Orders --> DDB3[(Order DB)]
    Orders --> SQS[SQS Queue]
    SQS --> Notify[Notification Service]`,
  },
]

export default function DiagramTemplates({
  templates = defaultTemplates,
  onSelectTemplate,
}: DiagramTemplatesProps) {
  const [previewTemplate, setPreviewTemplate] = useState<DiagramTemplate | null>(null)

  const handlePreview = (template: DiagramTemplate) => {
    setPreviewTemplate(template)
  }

  const handleClosePreview = () => {
    setPreviewTemplate(null)
  }

  const handleUseTemplate = (template: DiagramTemplate) => {
    onSelectTemplate(template)
    handleClosePreview()
  }

  return (
    <>
      <Grid container spacing={2}>
        {templates.map((template) => (
          <Grid item xs={12} sm={6} md={4} key={template.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': {
                  boxShadow: 4,
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" component="h3" gutterBottom>
                  {template.name}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 2, minHeight: 60 }}
                >
                  {template.description}
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  <Chip label={template.category} size="small" color="primary" />
                  {template.tags.slice(0, 2).map((tag) => (
                    <Chip key={tag} label={tag} size="small" variant="outlined" />
                  ))}
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<Visibility />}
                  onClick={() => handlePreview(template)}
                >
                  Preview
                </Button>
                <Button
                  size="small"
                  variant="contained"
                  onClick={() => handleUseTemplate(template)}
                >
                  Use Template
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Preview Dialog */}
      <Dialog
        open={Boolean(previewTemplate)}
        onClose={handleClosePreview}
        maxWidth="lg"
        fullWidth
      >
        {previewTemplate && (
          <>
            <DialogTitle>
              {previewTemplate.name}
              <Typography variant="body2" color="text.secondary">
                {previewTemplate.description}
              </Typography>
            </DialogTitle>
            <DialogContent>
              <ArchitectureVisualizer
                chart={previewTemplate.diagram}
                title="Template Preview"
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClosePreview}>Close</Button>
              <Button
                variant="contained"
                onClick={() => handleUseTemplate(previewTemplate)}
              >
                Use This Template
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </>
  )
}
