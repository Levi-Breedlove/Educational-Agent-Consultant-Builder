import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Button,
  Drawer,
  IconButton,
  Tooltip,
  Alert,
  Stack,
  useTheme,
  useMediaQuery,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
} from '@mui/material'
import {
  ViewModule,
  Close,
  Info,
  Visibility,
} from '@mui/icons-material'
import AWSArchitectureDiagram from './AWSArchitectureDiagram'
import { awsArchitectureTemplates, type AWSArchitectureTemplate } from './AWSArchitectureTemplates'

interface ArchitectureTabProps {
  generatedTemplate?: AWSArchitectureTemplate
  onTemplateUpdate?: (template: AWSArchitectureTemplate) => void
}

export default function ArchitectureTab({
  generatedTemplate,
  onTemplateUpdate,
}: ArchitectureTabProps) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const [templatesOpen, setTemplatesOpen] = useState(false)
  const [previewTemplate, setPreviewTemplate] = useState<AWSArchitectureTemplate | null>(null)
  const [currentTemplate, setCurrentTemplate] = useState<AWSArchitectureTemplate | null>(
    generatedTemplate || null
  )

  const handleTemplateSelect = (template: AWSArchitectureTemplate) => {
    setCurrentTemplate(template)
    setTemplatesOpen(false)
    setPreviewTemplate(null)
    if (onTemplateUpdate) {
      onTemplateUpdate(template)
    }
  }

  const handlePreview = (template: AWSArchitectureTemplate) => {
    setPreviewTemplate(template)
  }

  const handleClosePreview = () => {
    setPreviewTemplate(null)
  }

  return (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Header with controls */}
      <Box
        sx={{
          p: 2,
          borderBottom: 1,
          borderColor: 'divider',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexShrink: 0,
        }}
      >
        <Box>
          <Typography variant="h6" component="h2">
            AWS Architecture Diagram
          </Typography>
          {currentTemplate && (
            <Typography variant="caption" color="text.secondary">
              Template: {currentTemplate.name}
            </Typography>
          )}
        </Box>
        <Stack direction="row" spacing={1}>
          <Tooltip title="Browse AWS Templates">
            <Button
              variant="outlined"
              size="small"
              startIcon={<ViewModule />}
              onClick={() => setTemplatesOpen(true)}
            >
              {isMobile ? 'Templates' : 'Browse Templates'}
            </Button>
          </Tooltip>
        </Stack>
      </Box>

      {/* Main content area */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {currentTemplate ? (
          <AWSArchitectureDiagram
            services={currentTemplate.services}
            connections={currentTemplate.connections}
            title={currentTemplate.name}
            height={500}
          />
        ) : (
          <Paper
            sx={{
              p: 4,
              textAlign: 'center',
              bgcolor: 'background.default',
              border: 1,
              borderColor: 'divider',
              borderStyle: 'dashed',
            }}
          >
            <Info sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              No Architecture Diagram Yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Your AWS architecture diagram will appear here once the AI consultants design your solution.
              In the meantime, you can browse professional templates with official AWS icons.
            </Typography>
            <Button
              variant="contained"
              startIcon={<ViewModule />}
              onClick={() => setTemplatesOpen(true)}
            >
              Browse AWS Templates
            </Button>
          </Paper>
        )}

        {/* Info alert */}
        {currentTemplate && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              <strong>Professional AWS Architecture:</strong> This diagram uses official AWS service icons.
              Hover over services for descriptions. Click to view service details.
            </Typography>
          </Alert>
        )}
      </Box>

      {/* Templates Drawer */}
      <Drawer
        anchor={isMobile ? 'bottom' : 'right'}
        open={templatesOpen}
        onClose={() => setTemplatesOpen(false)}
        PaperProps={{
          sx: {
            width: isMobile ? '100%' : 700,
            maxWidth: '100%',
            height: isMobile ? '85vh' : '100%',
          },
        }}
      >
        <Box
          sx={{
            p: 2,
            borderBottom: 1,
            borderColor: 'divider',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <Box>
            <Typography variant="h6">AWS Architecture Templates</Typography>
            <Typography variant="caption" color="text.secondary">
              Professional templates with official AWS icons
            </Typography>
          </Box>
          <IconButton onClick={() => setTemplatesOpen(false)} size="small">
            <Close />
          </IconButton>
        </Box>
        <Box sx={{ p: 2, overflow: 'auto' }}>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              These templates use <strong>official AWS service icons</strong> and demonstrate
              production-ready architecture patterns following AWS best practices.
            </Typography>
          </Alert>
          
          <Grid container spacing={2}>
            {awsArchitectureTemplates.map((template) => (
              <Grid item xs={12} sm={6} key={template.id}>
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
                      onClick={() => handleTemplateSelect(template)}
                    >
                      Use Template
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Drawer>

      {/* Preview Dialog */}
      {previewTemplate && (
        <Drawer
          anchor="right"
          open={Boolean(previewTemplate)}
          onClose={handleClosePreview}
          PaperProps={{
            sx: {
              width: isMobile ? '100%' : 900,
              maxWidth: '100%',
            },
          }}
        >
          <Box
            sx={{
              p: 2,
              borderBottom: 1,
              borderColor: 'divider',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Box>
              <Typography variant="h6">{previewTemplate.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {previewTemplate.description}
              </Typography>
            </Box>
            <Stack direction="row" spacing={1}>
              <Button
                variant="contained"
                onClick={() => handleTemplateSelect(previewTemplate)}
              >
                Use This Template
              </Button>
              <IconButton onClick={handleClosePreview} size="small">
                <Close />
              </IconButton>
            </Stack>
          </Box>
          <Box sx={{ p: 3, overflow: 'auto' }}>
            <AWSArchitectureDiagram
              services={previewTemplate.services}
              connections={previewTemplate.connections}
              title="Template Preview"
              height={600}
            />
            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle2" gutterBottom>
                AWS Services Used:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                {previewTemplate.tags.map((tag) => (
                  <Chip key={tag} label={tag} size="small" color="primary" variant="outlined" />
                ))}
              </Box>
            </Box>
          </Box>
        </Drawer>
      )}
    </Box>
  )
}
