import { useState, useMemo, useRef, useEffect } from 'react'
import {
  Box,
  Paper,
  IconButton,
  Tooltip,
  Stack,
  Menu,
  MenuItem,
  Typography,
  Divider,
  ToggleButtonGroup,
  ToggleButton,
  Snackbar,
  Alert,
  Chip,
} from '@mui/material'
import {
  Download,
  ContentCopy,
  Fullscreen,
  FullscreenExit,
  Settings,
  WrapText,
  Save,
  Edit,
  Lock,
} from '@mui/icons-material'
import CodeMirror, { ReactCodeMirrorRef } from '@uiw/react-codemirror'
import { EditorView } from '@codemirror/view'
import { Extension } from '@codemirror/state'

// Language imports
import { javascript } from '@codemirror/lang-javascript'
import { python } from '@codemirror/lang-python'
import { json } from '@codemirror/lang-json'
import { yaml } from '@codemirror/lang-yaml'
import { markdown } from '@codemirror/lang-markdown'
import { html } from '@codemirror/lang-html'
import { css } from '@codemirror/lang-css'
import { sql } from '@codemirror/lang-sql'

// Theme import
import { oneDark } from '@codemirror/theme-one-dark'

interface CodePreviewV2Props {
  code: string
  language: string
  filename?: string
  readOnly?: boolean
  onChange?: (value: string) => void
  onSave?: (value: string) => void
  theme?: 'dark' | 'light'
  showHeader?: boolean
  enableEdit?: boolean // Allow toggling between read-only and editable
}

export default function CodePreviewV2({
  code,
  language,
  filename,
  readOnly = true,
  onChange,
  onSave,
  theme = 'dark',
  showHeader = true,
  enableEdit = false,
}: CodePreviewV2Props) {
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [settingsAnchor, setSettingsAnchor] = useState<null | HTMLElement>(null)
  const [wordWrap, setWordWrap] = useState(false)
  const [fontSize, setFontSize] = useState(14)
  const [copied, setCopied] = useState(false)
  const [isEditing, setIsEditing] = useState(!readOnly && enableEdit)
  const [currentCode, setCurrentCode] = useState(code)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const editorRef = useRef<ReactCodeMirrorRef>(null)

  // Update current code when prop changes
  useEffect(() => {
    setCurrentCode(code)
    setHasUnsavedChanges(false)
  }, [code])

  // Get language extension
  const getLanguageExtension = (lang: string): Extension | null => {
    const langLower = lang.toLowerCase()
    switch (langLower) {
      case 'javascript':
      case 'js':
        return javascript({ jsx: false, typescript: false })
      case 'typescript':
      case 'ts':
        return javascript({ jsx: false, typescript: true })
      case 'jsx':
        return javascript({ jsx: true, typescript: false })
      case 'tsx':
        return javascript({ jsx: true, typescript: true })
      case 'python':
      case 'py':
        return python()
      case 'json':
        return json()
      case 'yaml':
      case 'yml':
        return yaml()
      case 'markdown':
      case 'md':
        return markdown()
      case 'html':
        return html()
      case 'css':
        return css()
      case 'sql':
        return sql()
      default:
        return null
    }
  }

  // Build extensions array
  const extensions = useMemo(() => {
    const exts: Extension[] = []
    
    // Add language support
    const langExt = getLanguageExtension(language)
    if (langExt) {
      exts.push(langExt)
    }

    // Add word wrap
    if (wordWrap) {
      exts.push(EditorView.lineWrapping)
    }

    // Add read-only if needed
    if (!isEditing) {
      exts.push(EditorView.editable.of(false))
    }

    return exts
  }, [language, wordWrap, isEditing])

  // Custom theme with Node.js green accents
  const customTheme = useMemo(() => {
    if (theme === 'light') {
      return EditorView.theme({
        '&': {
          backgroundColor: '#ffffff',
          color: '#24292e',
          fontSize: `${fontSize}px`,
        },
        '.cm-content': {
          caretColor: '#68a063', // Node.js green
          fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
        },
        '.cm-cursor, .cm-dropCursor': {
          borderLeftColor: '#68a063',
        },
        '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
          backgroundColor: '#68a06333',
        },
        '.cm-activeLine': {
          backgroundColor: '#f6f8fa',
        },
        '.cm-gutters': {
          backgroundColor: '#f6f8fa',
          color: '#6a737d',
          border: 'none',
        },
        '.cm-activeLineGutter': {
          backgroundColor: '#e1e4e8',
        },
      }, { dark: false })
    }

    // Dark theme with Node.js green accents
    return EditorView.theme({
      '&': {
        backgroundColor: '#1e1e1e',
        color: '#d4d4d4',
        fontSize: `${fontSize}px`,
      },
      '.cm-content': {
        caretColor: '#68a063', // Node.js green
        fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
      },
      '.cm-cursor, .cm-dropCursor': {
        borderLeftColor: '#68a063',
      },
      '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
        backgroundColor: '#68a06333',
      },
      '.cm-activeLine': {
        backgroundColor: '#2a2a2a',
      },
      '.cm-gutters': {
        backgroundColor: '#1e1e1e',
        color: '#858585',
        border: 'none',
      },
      '.cm-activeLineGutter': {
        backgroundColor: '#2a2a2a',
        color: '#68a063',
      },
      '.cm-lineNumbers .cm-gutterElement': {
        padding: '0 8px 0 5px',
      },
    }, { dark: true })
  }, [theme, fontSize])

  const handleCodeChange = (value: string) => {
    setCurrentCode(value)
    setHasUnsavedChanges(value !== code)
    onChange?.(value)
  }

  const handleSave = () => {
    if (onSave && hasUnsavedChanges) {
      onSave(currentCode)
      setHasUnsavedChanges(false)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    }
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(currentCode)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  const handleDownload = () => {
    const blob = new Blob([currentCode], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.download = filename || `code.${getFileExtension(language)}`
    link.href = url
    link.click()
    URL.revokeObjectURL(url)
  }

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  const toggleEditMode = () => {
    if (enableEdit) {
      setIsEditing(!isEditing)
    }
  }

  const handleSettingsClick = (event: React.MouseEvent<HTMLElement>) => {
    setSettingsAnchor(event.currentTarget)
  }

  const handleSettingsClose = () => {
    setSettingsAnchor(null)
  }

  const toggleWordWrap = () => {
    setWordWrap(!wordWrap)
  }

  const handleFontSizeChange = (_: React.MouseEvent<HTMLElement>, newSize: number | null) => {
    if (newSize !== null) {
      setFontSize(newSize)
    }
  }

  return (
    <Paper
      elevation={0}
      sx={{
        bgcolor: 'background.default',
        border: showHeader ? 1 : 0,
        borderColor: 'divider',
        position: isFullscreen ? 'fixed' : 'relative',
        top: isFullscreen ? 0 : 'auto',
        left: isFullscreen ? 0 : 'auto',
        right: isFullscreen ? 0 : 'auto',
        bottom: isFullscreen ? 0 : 'auto',
        zIndex: isFullscreen ? 1300 : 'auto',
        display: 'flex',
        flexDirection: 'column',
        height: isFullscreen ? '100vh' : '100%',
        minHeight: isFullscreen ? '100vh' : 400,
      }}
    >
      {/* Header with controls */}
      {showHeader && (
        <Box
          sx={{
            p: 2,
            borderBottom: 1,
            borderColor: 'divider',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexShrink: 0,
            bgcolor: 'background.paper',
            position: 'relative',
            zIndex: 1,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {filename && (
              <Typography variant="subtitle2" component="h3">
                {filename}
              </Typography>
            )}
            <Typography variant="caption" color="text.secondary">
              {language.toUpperCase()}
            </Typography>
            {hasUnsavedChanges && (
              <Chip label="Unsaved" size="small" color="warning" />
            )}
            {isEditing && (
              <Chip label="Editing" size="small" color="primary" icon={<Edit />} />
            )}
          </Box>
          <Stack direction="row" spacing={1}>
            {enableEdit && (
              <Tooltip title={isEditing ? 'Lock (Read-Only)' : 'Edit'}>
                <IconButton size="small" onClick={toggleEditMode} color={isEditing ? 'primary' : 'default'}>
                  {isEditing ? <Edit /> : <Lock />}
                </IconButton>
              </Tooltip>
            )}
            {isEditing && onSave && (
              <Tooltip title="Save Changes">
                <IconButton 
                  size="small" 
                  onClick={handleSave}
                  disabled={!hasUnsavedChanges}
                  color={hasUnsavedChanges ? 'primary' : 'default'}
                >
                  <Save />
                </IconButton>
              </Tooltip>
            )}
            <Tooltip title={copied ? 'Copied!' : 'Copy Code'}>
              <IconButton size="small" onClick={handleCopy}>
                <ContentCopy />
              </IconButton>
            </Tooltip>
            <Tooltip title="Download">
              <IconButton size="small" onClick={handleDownload}>
                <Download />
              </IconButton>
            </Tooltip>
            <Divider orientation="vertical" flexItem />
            <Tooltip title="Settings">
              <IconButton size="small" onClick={handleSettingsClick}>
                <Settings />
              </IconButton>
            </Tooltip>
            <Tooltip title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}>
              <IconButton size="small" onClick={toggleFullscreen}>
                {isFullscreen ? <FullscreenExit /> : <Fullscreen />}
              </IconButton>
            </Tooltip>
          </Stack>
        </Box>
      )}

      {/* Settings Menu */}
      <Menu
        anchorEl={settingsAnchor}
        open={Boolean(settingsAnchor)}
        onClose={handleSettingsClose}
      >
        <MenuItem onClick={toggleWordWrap}>
          <WrapText sx={{ mr: 1 }} />
          Word Wrap: {wordWrap ? 'On' : 'Off'}
        </MenuItem>
        <Divider />
        <Box sx={{ px: 2, py: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Font Size
          </Typography>
          <ToggleButtonGroup
            value={fontSize}
            exclusive
            onChange={handleFontSizeChange}
            size="small"
            sx={{ mt: 1 }}
          >
            <ToggleButton value={12}>12</ToggleButton>
            <ToggleButton value={14}>14</ToggleButton>
            <ToggleButton value={16}>16</ToggleButton>
            <ToggleButton value={18}>18</ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Menu>

      {/* CodeMirror Editor */}
      <Box
        sx={{
          flex: 1,
          minHeight: 0,
          overflow: 'auto',
          position: 'relative',
          bgcolor: theme === 'dark' ? '#1e1e1e' : '#ffffff',
          '& .cm-editor': {
            height: '100%',
          },
          '& .cm-scroller': {
            overflow: 'auto',
            fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
          },
        }}
      >
        <CodeMirror
          ref={editorRef}
          value={currentCode}
          height="100%"
          theme={theme === 'dark' ? oneDark : 'light'}
          extensions={[...extensions, customTheme]}
          onChange={handleCodeChange}
          basicSetup={{
            lineNumbers: true,
            highlightActiveLineGutter: true,
            highlightSpecialChars: true,
            history: isEditing,
            foldGutter: true,
            drawSelection: true,
            dropCursor: isEditing,
            allowMultipleSelections: isEditing,
            indentOnInput: isEditing,
            syntaxHighlighting: true,
            bracketMatching: true,
            closeBrackets: isEditing,
            autocompletion: isEditing,
            rectangularSelection: isEditing,
            crosshairCursor: isEditing,
            highlightActiveLine: isEditing,
            highlightSelectionMatches: isEditing,
            closeBracketsKeymap: isEditing,
            defaultKeymap: true,
            searchKeymap: true,
            historyKeymap: isEditing,
            foldKeymap: true,
            completionKeymap: isEditing,
            lintKeymap: isEditing,
          }}
        />
      </Box>

      {/* Save Success Snackbar */}
      <Snackbar
        open={saveSuccess}
        autoHideDuration={3000}
        onClose={() => setSaveSuccess(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert severity="success" variant="filled">
          Changes saved successfully!
        </Alert>
      </Snackbar>
    </Paper>
  )
}

// Helper function to get file extension from language
function getFileExtension(language: string): string {
  const extensions: Record<string, string> = {
    javascript: 'js',
    js: 'js',
    typescript: 'ts',
    ts: 'ts',
    jsx: 'jsx',
    tsx: 'tsx',
    python: 'py',
    py: 'py',
    yaml: 'yaml',
    yml: 'yml',
    json: 'json',
    html: 'html',
    css: 'css',
    markdown: 'md',
    md: 'md',
    shell: 'sh',
    bash: 'sh',
    sh: 'sh',
    sql: 'sql',
  }
  return extensions[language.toLowerCase()] || 'txt'
}
