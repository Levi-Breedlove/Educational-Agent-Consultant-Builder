import { useState } from 'react'
import { Box, Grid, Paper, Tabs, Tab, Typography, Chip, Button, Stack } from '@mui/material'
import { Download } from '@mui/icons-material'
import JSZip from 'jszip'
import FileTreeNavigator, { FileNode, buildFileTree } from './FileTreeNavigator'
import CodePreviewV2 from './CodePreviewV2'
import CodeDiffViewerV2 from './CodeDiffViewerV2'

interface CodeWorkspaceProps {
  files: Array<{
    path: string
    content: string
    language: string
  }>
  title?: string
  showDiff?: boolean
  originalFiles?: Array<{
    path: string
    content: string
    language: string
  }>
}

type ViewMode = 'preview' | 'diff'

export default function CodeWorkspace({
  files,
  title = 'Generated Code',
  showDiff = false,
  originalFiles,
}: CodeWorkspaceProps) {
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null)
  const [viewMode, setViewMode] = useState<ViewMode>('preview')

  const fileTree = buildFileTree(files)

  const handleFileSelect = (file: FileNode) => {
    setSelectedFile(file)
  }

  const handleViewModeChange = (_: React.SyntheticEvent, newMode: ViewMode) => {
    setViewMode(newMode)
  }

  const getOriginalFileContent = (path: string): string | undefined => {
    return originalFiles?.find((f) => f.path === path)?.content
  }

  const getFileStats = () => {
    const totalFiles = files.length
    const languages = new Set(files.map((f) => f.language))
    const totalLines = files.reduce(
      (sum, f) => sum + f.content.split('\n').length,
      0
    )
    return { totalFiles, languages: Array.from(languages), totalLines }
  }

  const stats = getFileStats()

  const handleDownloadAll = async () => {
    const zip = new JSZip()

    // Add all files to the ZIP
    files.forEach((file) => {
      // Remove leading slash if present
      const filePath = file.path.startsWith('/') ? file.path.slice(1) : file.path
      zip.file(filePath, file.content)
    })

    // Generate the ZIP file
    const blob = await zip.generateAsync({ type: 'blob' })
    
    // Create download link
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.download = `${title.toLowerCase().replace(/\s+/g, '-')}.zip`
    link.href = url
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <Paper
      elevation={0}
      sx={{
        border: 1,
        borderColor: 'divider',
        overflow: 'hidden',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: 1,
          borderColor: 'divider',
          bgcolor: 'background.paper',
          flexShrink: 0,
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h6" component="h2">
            {title}
          </Typography>
          <Stack direction="row" spacing={1} alignItems="center">
            <Chip label={`${stats.totalFiles} files`} size="small" />
            <Chip label={`${stats.totalLines.toLocaleString()} lines`} size="small" />
            <Chip
              label={`${stats.languages.length} language${stats.languages.length !== 1 ? 's' : ''}`}
              size="small"
            />
            <Button
              variant="contained"
              size="small"
              startIcon={<Download />}
              onClick={handleDownloadAll}
              sx={{ ml: 1 }}
            >
              Download All
            </Button>
          </Stack>
        </Box>

        {showDiff && originalFiles && (
          <Tabs value={viewMode} onChange={handleViewModeChange}>
            <Tab label="Preview" value="preview" />
            <Tab label="Compare Changes" value="diff" />
          </Tabs>
        )}
      </Box>

      {/* Main Content */}
      <Grid container sx={{ flex: 1, minHeight: 0 }}>
        {/* File Tree Sidebar */}
        <Grid
          item
          xs={12}
          md={3}
          sx={{
            borderRight: { md: 1 },
            borderColor: 'divider',
            height: '100%',
            overflow: 'auto',
          }}
        >
          <FileTreeNavigator
            files={fileTree}
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile || undefined}
          />
        </Grid>

        {/* Code Preview Area */}
        <Grid
          item
          xs={12}
          md={9}
          sx={{
            height: '100%',
            overflow: 'hidden',
            bgcolor: 'background.default',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {selectedFile ? (
            <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              {viewMode === 'preview' ? (
                <CodePreviewV2
                  code={selectedFile.content || ''}
                  language={selectedFile.language || 'text'}
                  filename={selectedFile.name}
                  readOnly={false}
                  enableEdit={true}
                  showHeader={true}
                  showMinimap={true}
                  onChange={(value) => {
                    // Update file content in state
                    if (selectedFile) {
                      selectedFile.content = value
                    }
                  }}
                  onSave={(value) => {
                    console.log('Saving file:', selectedFile.name, value.length, 'characters')
                    // TODO: Implement actual save functionality
                  }}
                />
              ) : (
                showDiff &&
                originalFiles && (
                  <CodeDiffViewerV2
                    originalCode={getOriginalFileContent(selectedFile.path) || ''}
                    modifiedCode={selectedFile.content || ''}
                    language={selectedFile.language || 'text'}
                    originalLabel="Previous Version"
                    modifiedLabel="Current Version"
                  />
                )
              )}
            </Box>
          ) : (
            <Box
              sx={{
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'text.secondary',
              }}
            >
              <Typography variant="body1">
                Select a file from the tree to preview
              </Typography>
            </Box>
          )}
        </Grid>
      </Grid>
    </Paper>
  )
}
