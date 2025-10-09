import { useState } from 'react'
import { Box, IconButton, Typography, Tooltip } from '@mui/material'
import { ContentCopy, Check } from '@mui/icons-material'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-yaml'
import 'prismjs/components/prism-markdown'

interface CodeBlockProps {
  code: string
  language: string
}

export default function CodeBlock({ code, language }: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // Highlight code
  const highlightedCode = Prism.highlight(
    code,
    Prism.languages[language] || Prism.languages.text,
    language
  )

  return (
    <Box
      sx={{
        position: 'relative',
        my: 2,
        borderRadius: 1,
        overflow: 'hidden',
        bgcolor: '#2d2d2d',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          px: 2,
          py: 1,
          bgcolor: '#1e1e1e',
          borderBottom: '1px solid #404040',
        }}
      >
        <Typography variant="caption" sx={{ color: '#888', textTransform: 'uppercase' }}>
          {language}
        </Typography>
        <Tooltip title={copied ? 'Copied!' : 'Copy code'}>
          <IconButton size="small" onClick={handleCopy} sx={{ color: '#888' }}>
            {copied ? <Check fontSize="small" /> : <ContentCopy fontSize="small" />}
          </IconButton>
        </Tooltip>
      </Box>

      {/* Code */}
      <Box
        component="pre"
        sx={{
          m: 0,
          p: 2,
          overflow: 'auto',
          fontSize: '0.875rem',
          lineHeight: 1.5,
          '& code': {
            fontFamily: '"Fira Code", "Courier New", monospace',
          },
        }}
      >
        <code
          className={`language-${language}`}
          dangerouslySetInnerHTML={{ __html: highlightedCode }}
        />
      </Box>
    </Box>
  )
}
