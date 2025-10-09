import { useState, useMemo } from 'react'
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Tooltip,
  Stack,
  ToggleButtonGroup,
  ToggleButton,
  Divider,
} from '@mui/material'
import {
  Fullscreen,
  FullscreenExit,
  SwapHoriz,
  Download,
} from '@mui/icons-material'
import CodeMirror from '@uiw/react-codemirror'
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

interface CodeDiffViewerV2Props {
  originalCode: string
  modifiedCode: string
  language: string
  originalLabel?: string
  modifiedLabel?: string
  theme?: 'dark' | 'light'
}

interface DiffLine {
  type: 'added' | 'removed' | 'modified' | 'unchanged'
  originalLine: string
  modifiedLine: string
  originalLineNumber: number
  modifiedLineNumber: number
}

export default function CodeDiffViewerV2({
  originalCode,
  modifiedCode,
  language,
  originalLabel = 'Original',
  modifiedLabel = 'Modified',
  theme = 'dark',
}: CodeDiffViewerV2Props) {
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [renderSideBySide, setRenderSideBySide] = useState(true)
  const [swapped, setSwapped] = useState(false)

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

  // Simple diff algorithm
  const computeDiff = (original: string, modified: string): DiffLine[] => {
    const originalLines = original.split('\n')
    const modifiedLines = modified.split('\n')
    const diff: DiffLine[] = []

    let origIndex = 0
    let modIndex = 0

    while (origIndex < originalLines.length || modIndex < modifiedLines.length) {
      const origLine = originalLines[origIndex] || ''
      const modLine = modifiedLines[modIndex] || ''

      if (origIndex >= originalLines.length) {
        // Only modified lines left
        diff.push({
          type: 'added',
          originalLine: '',
          modifiedLine: modLine,
          originalLineNumber: -1,
          modifiedLineNumber: modIndex + 1,
        })
        modIndex++
      } else if (modIndex >= modifiedLines.length) {
        // Only original lines left
        diff.push({
          type: 'removed',
          originalLine: origLine,
          modifiedLine: '',
          originalLineNumber: origIndex + 1,
          modifiedLineNumber: -1,
        })
        origIndex++
      } else if (origLine === modLine) {
        // Lines are the same
        diff.push({
          type: 'unchanged',
          originalLine: origLine,
          modifiedLine: modLine,
          originalLineNumber: origIndex + 1,
          modifiedLineNumber: modIndex + 1,
        })
        origIndex++
        modIndex++
      } else {
        // Lines are different - check if it's a modification or add/remove
        const nextOrigMatch = modifiedLines.slice(modIndex + 1).indexOf(origLine)
        const nextModMatch = originalLines.slice(origIndex + 1).indexOf(modLine)

        if (nextOrigMatch === -1 && nextModMatch === -1) {
          // Likely a modification
          diff.push({
            type: 'modified',
            originalLine: origLine,
            modifiedLine: modLine,
            originalLineNumber: origIndex + 1,
            modifiedLineNumber: modIndex + 1,
          })
          origIndex++
          modIndex++
        } else if (nextOrigMatch !== -1 && (nextModMatch === -1 || nextOrigMatch < nextModMatch)) {
          // Line was added
          diff.push({
            type: 'added',
            originalLine: '',
            modifiedLine: modLine,
            originalLineNumber: -1,
            modifiedLineNumber: modIndex + 1,
          })
          modIndex++
        } else {
          // Line was removed
          diff.push({
            type: 'removed',
            originalLine: origLine,
            modifiedLine: '',
            originalLineNumber: origIndex + 1,
            modifiedLineNumber: -1,
          })
          origIndex++
        }
      }
    }

    return diff
  }

  // Build extensions array
  const extensions = useMemo(() => {
    const exts: Extension[] = []
    
    // Add language support
    const langExt = getLanguageExtension(language)
    if (langExt) {
      exts.push(langExt)
    }

    // Add read-only
    exts.push(EditorView.editable.of(false))

    return exts
  }, [language])

  // Custom theme with Node.js green accents and diff colors
  const customTheme = useMemo(() => {
    if (theme === 'light') {
      return EditorView.theme({
        '&': {
          backgroundColor: '#ffffff',
          color: '#24292e',
          fontSize: '14px',
        },
        '.cm-content': {
          fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
        },
        '.cm-gutters': {
          backgroundColor: '#f6f8fa',
          color: '#6a737d',
          border: 'none',
        },
        '.cm-line-added': {
          backgroundColor: '#e6ffed',
        },
        '.cm-line-removed': {
          backgroundColor: '#ffeef0',
        },
        '.cm-line-modified': {
          backgroundColor: '#fff8e6',
        },
      }, { dark: false })
    }

    // Dark theme with diff colors
    return EditorView.theme({
      '&': {
        backgroundColor: '#1e1e1e',
        color: '#d4d4d4',
        fontSize: '14px',
      },
      '.cm-content': {
        fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
      },
      '.cm-gutters': {
        backgroundColor: '#1e1e1e',
        color: '#858585',
        border: 'none',
      },
      '.cm-line-added': {
        backgroundColor: 'rgba(46, 160, 67, 0.15)',
      },
      '.cm-line-removed': {
        backgroundColor: 'rgba(248, 81, 73, 0.15)',
      },
      '.cm-line-modified': {
        backgroundColor: 'rgba(255, 191, 0, 0.15)',
      },
    }, { dark: true })
  }, [theme])

  const displayOriginal = swapped ? modifiedCode : originalCode
  const displayModified = swapped ? originalCode : modifiedCode
  const displayOriginalLabel = swapped ? modifiedLabel : originalLabel
  const displayModifiedLabel = swapped ? originalLabel : modifiedLabel

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  const toggleRenderMode = (
    _: React.MouseEvent<HTMLElement>,
    newMode: 'side-by-side' | 'inline' | null
  ) => {
    if (newMode !== null) {
      setRenderSideBySide(newMode === 'side-by-side')
    }
  }

  const handleSwap = () => {
    setSwapped(!swapped)
  }

  const handleDownloadDiff = () => {
    const diffText = `
=== ${displayOriginalLabel} ===
${displayOriginal}

=== ${displayModifiedLabel} ===
${displayModified}
    `.trim()

    const blob = new Blob([diffText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.download = `diff-${Date.now()}.txt`
    link.href = url
    link.click()
    URL.revokeObjectURL(url)
  }

  // Compute diff for inline mode
  const diff = useMemo(() => {
    if (!renderSideBySide) {
      return computeDiff(displayOriginal, displayModified)
    }
    return []
  }, [displayOriginal, displayModified, renderSideBySide])

  // Build inline diff view
  const inlineDiffContent = useMemo(() => {
    if (renderSideBySide) return ''
    
    return diff.map(line => {
      if (line.type === 'removed') {
        return `- ${line.originalLine}`
      } else if (line.type === 'added') {
        return `+ ${line.modifiedLine}`
      } else if (line.type === 'modified') {
        return `~ ${line.modifiedLine}`
      } else {
        return `  ${line.originalLine}`
      }
    }).join('\n')
  }, [diff, renderSideBySide])

  return (
    <Paper
      elevation={0}
      sx={{
        bgcolor: 'background.default',
        border: 1,
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
        minHeight: isFullscreen ? '100vh' : 500,
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
          bgcolor: 'background.paper',
          position: 'relative',
          zIndex: 1,
        }}
      >
        <Box>
          <Typography variant="h6" component="h3">
            Code Comparison
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {displayOriginalLabel} vs {displayModifiedLabel}
          </Typography>
        </Box>
        <Stack direction="row" spacing={1} alignItems="center">
          <ToggleButtonGroup
            value={renderSideBySide ? 'side-by-side' : 'inline'}
            exclusive
            onChange={toggleRenderMode}
            size="small"
          >
            <ToggleButton value="side-by-side">Side by Side</ToggleButton>
            <ToggleButton value="inline">Inline</ToggleButton>
          </ToggleButtonGroup>
          <Divider orientation="vertical" flexItem />
          <Tooltip title="Swap Sides">
            <IconButton size="small" onClick={handleSwap}>
              <SwapHoriz />
            </IconButton>
          </Tooltip>
          <Tooltip title="Download Diff">
            <IconButton size="small" onClick={handleDownloadDiff}>
              <Download />
            </IconButton>
          </Tooltip>
          <Tooltip title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}>
            <IconButton size="small" onClick={toggleFullscreen}>
              {isFullscreen ? <FullscreenExit /> : <Fullscreen />}
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {/* Diff View */}
      <Box
        sx={{
          flex: 1,
          minHeight: 0,
          overflow: 'hidden',
          position: 'relative',
          bgcolor: theme === 'dark' ? '#1e1e1e' : '#ffffff',
          display: 'flex',
        }}
      >
        {renderSideBySide ? (
          <>
            {/* Side-by-side view */}
            <Box
              sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                borderRight: 1,
                borderColor: 'divider',
                overflow: 'hidden',
              }}
            >
              <Box
                sx={{
                  p: 1,
                  bgcolor: theme === 'dark' ? '#252525' : '#f6f8fa',
                  borderBottom: 1,
                  borderColor: 'divider',
                }}
              >
                <Typography variant="caption" fontWeight="bold">
                  {displayOriginalLabel}
                </Typography>
              </Box>
              <Box sx={{ flex: 1, overflow: 'auto' }}>
                <CodeMirror
                  value={displayOriginal}
                  height="100%"
                  theme={theme === 'dark' ? oneDark : 'light'}
                  extensions={[...extensions, customTheme]}
                  basicSetup={{
                    lineNumbers: true,
                    highlightActiveLineGutter: false,
                    highlightSpecialChars: true,
                    history: false,
                    foldGutter: true,
                    drawSelection: true,
                    dropCursor: false,
                    allowMultipleSelections: false,
                    indentOnInput: false,
                    syntaxHighlighting: true,
                    bracketMatching: true,
                    closeBrackets: false,
                    autocompletion: false,
                    rectangularSelection: false,
                    crosshairCursor: false,
                    highlightActiveLine: false,
                    highlightSelectionMatches: false,
                    closeBracketsKeymap: false,
                    defaultKeymap: true,
                    searchKeymap: true,
                    historyKeymap: false,
                    foldKeymap: true,
                    completionKeymap: false,
                    lintKeymap: false,
                  }}
                />
              </Box>
            </Box>
            <Box
              sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              <Box
                sx={{
                  p: 1,
                  bgcolor: theme === 'dark' ? '#252525' : '#f6f8fa',
                  borderBottom: 1,
                  borderColor: 'divider',
                }}
              >
                <Typography variant="caption" fontWeight="bold">
                  {displayModifiedLabel}
                </Typography>
              </Box>
              <Box sx={{ flex: 1, overflow: 'auto' }}>
                <CodeMirror
                  value={displayModified}
                  height="100%"
                  theme={theme === 'dark' ? oneDark : 'light'}
                  extensions={[...extensions, customTheme]}
                  basicSetup={{
                    lineNumbers: true,
                    highlightActiveLineGutter: false,
                    highlightSpecialChars: true,
                    history: false,
                    foldGutter: true,
                    drawSelection: true,
                    dropCursor: false,
                    allowMultipleSelections: false,
                    indentOnInput: false,
                    syntaxHighlighting: true,
                    bracketMatching: true,
                    closeBrackets: false,
                    autocompletion: false,
                    rectangularSelection: false,
                    crosshairCursor: false,
                    highlightActiveLine: false,
                    highlightSelectionMatches: false,
                    closeBracketsKeymap: false,
                    defaultKeymap: true,
                    searchKeymap: true,
                    historyKeymap: false,
                    foldKeymap: true,
                    completionKeymap: false,
                    lintKeymap: false,
                  }}
                />
              </Box>
            </Box>
          </>
        ) : (
          <>
            {/* Inline view */}
            <Box
              sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              <Box
                sx={{
                  p: 1,
                  bgcolor: theme === 'dark' ? '#252525' : '#f6f8fa',
                  borderBottom: 1,
                  borderColor: 'divider',
                }}
              >
                <Typography variant="caption" fontWeight="bold">
                  Unified Diff
                </Typography>
              </Box>
              <Box sx={{ flex: 1, overflow: 'auto' }}>
                <CodeMirror
                  value={inlineDiffContent}
                  height="100%"
                  theme={theme === 'dark' ? oneDark : 'light'}
                  extensions={[...extensions, customTheme]}
                  basicSetup={{
                    lineNumbers: true,
                    highlightActiveLineGutter: false,
                    highlightSpecialChars: true,
                    history: false,
                    foldGutter: true,
                    drawSelection: true,
                    dropCursor: false,
                    allowMultipleSelections: false,
                    indentOnInput: false,
                    syntaxHighlighting: true,
                    bracketMatching: true,
                    closeBrackets: false,
                    autocompletion: false,
                    rectangularSelection: false,
                    crosshairCursor: false,
                    highlightActiveLine: false,
                    highlightSelectionMatches: false,
                    closeBracketsKeymap: false,
                    defaultKeymap: true,
                    searchKeymap: true,
                    historyKeymap: false,
                    foldKeymap: true,
                    completionKeymap: false,
                    lintKeymap: false,
                  }}
                />
              </Box>
            </Box>
          </>
        )}
      </Box>

      {/* Legend */}
      <Box
        sx={{
          p: 1,
          borderTop: 1,
          borderColor: 'divider',
          display: 'flex',
          gap: 2,
          justifyContent: 'center',
          bgcolor: 'background.paper',
          flexShrink: 0,
          position: 'relative',
          zIndex: 1,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 16,
              height: 16,
              bgcolor: theme === 'dark' ? 'rgba(248, 81, 73, 0.3)' : 'rgba(248, 81, 73, 0.2)',
              borderRadius: 0.5,
            }}
          />
          <Typography variant="caption">Removed</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 16,
              height: 16,
              bgcolor: theme === 'dark' ? 'rgba(46, 160, 67, 0.3)' : 'rgba(46, 160, 67, 0.2)',
              borderRadius: 0.5,
            }}
          />
          <Typography variant="caption">Added</Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Box
            sx={{
              width: 16,
              height: 16,
              bgcolor: theme === 'dark' ? 'rgba(255, 191, 0, 0.3)' : 'rgba(255, 191, 0, 0.2)',
              borderRadius: 0.5,
            }}
          />
          <Typography variant="caption">Modified</Typography>
        </Box>
      </Box>
    </Paper>
  )
}
