import { useState } from 'react'
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Typography,
  Paper,
  TextField,
  InputAdornment,
} from '@mui/material'
import {
  Folder,
  FolderOpen,
  InsertDriveFile,
  ExpandMore,
  ChevronRight,
  Search,
  Code,
  Description,
  Settings as SettingsIcon,
} from '@mui/icons-material'

export interface FileNode {
  name: string
  path: string
  type: 'file' | 'folder'
  children?: FileNode[]
  language?: string
  content?: string
}

interface FileTreeNavigatorProps {
  files: FileNode[]
  onFileSelect: (file: FileNode) => void
  selectedFile?: FileNode
}

export default function FileTreeNavigator({
  files,
  onFileSelect,
  selectedFile,
}: FileTreeNavigatorProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['/']))
  const [searchQuery, setSearchQuery] = useState('')

  const toggleFolder = (path: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev)
      if (next.has(path)) {
        next.delete(path)
      } else {
        next.add(path)
      }
      return next
    })
  }

  const getFileIcon = (file: FileNode) => {
    if (file.type === 'folder') {
      return expandedFolders.has(file.path) ? <FolderOpen /> : <Folder />
    }

    // Return icon based on file extension
    const ext = file.name.split('.').pop()?.toLowerCase()
    switch (ext) {
      case 'py':
      case 'js':
      case 'ts':
      case 'tsx':
      case 'jsx':
        return <Code />
      case 'yaml':
      case 'yml':
      case 'json':
        return <SettingsIcon />
      case 'md':
      case 'txt':
        return <Description />
      default:
        return <InsertDriveFile />
    }
  }

  const filterFiles = (nodes: FileNode[], query: string): FileNode[] => {
    if (!query) return nodes

    return nodes.reduce<FileNode[]>((acc, node) => {
      if (node.type === 'folder' && node.children) {
        const filteredChildren = filterFiles(node.children, query)
        if (filteredChildren.length > 0) {
          acc.push({ ...node, children: filteredChildren })
        }
      } else if (node.name.toLowerCase().includes(query.toLowerCase())) {
        acc.push(node)
      }
      return acc
    }, [])
  }

  const renderFileTree = (nodes: FileNode[], depth = 0) => {
    const filteredNodes = searchQuery ? filterFiles(nodes, searchQuery) : nodes

    return filteredNodes.map((node) => {
      const isExpanded = expandedFolders.has(node.path)
      const isSelected = selectedFile?.path === node.path

      return (
        <Box key={node.path}>
          <ListItem disablePadding>
            <ListItemButton
              selected={isSelected}
              onClick={() => {
                if (node.type === 'folder') {
                  toggleFolder(node.path)
                } else {
                  onFileSelect(node)
                }
              }}
              sx={{
                pl: 2 + depth * 2,
                '&.Mui-selected': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'primary.contrastText',
                  },
                },
              }}
            >
              {node.type === 'folder' && (
                <ListItemIcon sx={{ minWidth: 32 }}>
                  {isExpanded ? <ExpandMore /> : <ChevronRight />}
                </ListItemIcon>
              )}
              <ListItemIcon sx={{ minWidth: 36 }}>{getFileIcon(node)}</ListItemIcon>
              <ListItemText
                primary={node.name}
                primaryTypographyProps={{
                  variant: 'body2',
                  noWrap: true,
                }}
              />
            </ListItemButton>
          </ListItem>
          {node.type === 'folder' && node.children && (
            <Collapse in={isExpanded} timeout="auto" unmountOnExit>
              {renderFileTree(node.children, depth + 1)}
            </Collapse>
          )}
        </Box>
      )
    })
  }

  return (
    <Paper
      elevation={0}
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        border: 1,
        borderColor: 'divider',
      }}
    >
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          Files
        </Typography>
        <TextField
          fullWidth
          size="small"
          placeholder="Search files..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      {/* File Tree */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List dense disablePadding>
          {renderFileTree(files)}
        </List>
      </Box>
    </Paper>
  )
}

// Helper function to build file tree from flat file list
export function buildFileTree(files: Array<{ path: string; content: string; language: string }>): FileNode[] {
  const root: FileNode = {
    name: 'root',
    path: '/',
    type: 'folder',
    children: [],
  }

  files.forEach((file) => {
    const parts = file.path.split('/').filter(Boolean)
    let current = root

    parts.forEach((part, index) => {
      const isFile = index === parts.length - 1
      const path = '/' + parts.slice(0, index + 1).join('/')

      if (!current.children) {
        current.children = []
      }

      let node = current.children.find((n) => n.name === part)

      if (!node) {
        node = {
          name: part,
          path,
          type: isFile ? 'file' : 'folder',
          ...(isFile && {
            content: file.content,
            language: file.language,
          }),
        }
        current.children.push(node)
      }

      if (!isFile) {
        current = node
      }
    })
  })

  return root.children || []
}
