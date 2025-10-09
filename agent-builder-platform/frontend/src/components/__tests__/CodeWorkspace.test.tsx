import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import CodeWorkspace from '../CodeWorkspace'

describe('CodeWorkspace', () => {
  const mockFiles = [
    {
      path: '/test/file1.py',
      content: 'print("Hello, World!")',
      language: 'python',
    },
    {
      path: '/test/file2.ts',
      content: 'console.log("Hello, World!");',
      language: 'typescript',
    },
  ]

  it('renders without crashing', () => {
    render(<CodeWorkspace files={mockFiles} />)
    expect(screen.getByText('Generated Code')).toBeInTheDocument()
  })

  it('displays file statistics', () => {
    render(<CodeWorkspace files={mockFiles} />)
    expect(screen.getByText('2 files')).toBeInTheDocument()
    expect(screen.getByText('2 languages')).toBeInTheDocument()
  })

  it('shows empty state when no file is selected', () => {
    render(<CodeWorkspace files={mockFiles} />)
    expect(screen.getByText('Select a file from the tree to preview')).toBeInTheDocument()
  })

  it('renders with custom title', () => {
    render(<CodeWorkspace files={mockFiles} title="My Custom Code" />)
    expect(screen.getByText('My Custom Code')).toBeInTheDocument()
  })

  it('shows diff tab when showDiff is true and originalFiles provided', () => {
    const originalFiles = [
      {
        path: '/test/file1.py',
        content: 'print("Hello")',
        language: 'python',
      },
    ]
    render(
      <CodeWorkspace
        files={mockFiles}
        showDiff={true}
        originalFiles={originalFiles}
      />
    )
    expect(screen.getByText('Preview')).toBeInTheDocument()
    expect(screen.getByText('Compare Changes')).toBeInTheDocument()
  })

  it('does not show diff tab when showDiff is false', () => {
    render(<CodeWorkspace files={mockFiles} showDiff={false} />)
    expect(screen.queryByText('Compare Changes')).not.toBeInTheDocument()
  })
})
