import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import CodeDiffViewerV2 from '../CodeDiffViewerV2'

describe('CodeDiffViewerV2', () => {
  const originalCode = `function hello() {
  console.log('Hello');
  return true;
}`

  const modifiedCode = `function hello() {
  console.log('Hello World');
  console.log('Modified');
  return true;
}`

  it('renders with default props', () => {
    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
      />
    )

    expect(screen.getByText('Code Comparison')).toBeInTheDocument()
    expect(screen.getByText(/Original vs Modified/i)).toBeInTheDocument()
  })

  it('renders with custom labels', () => {
    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
        originalLabel="Version 1"
        modifiedLabel="Version 2"
      />
    )

    expect(screen.getByText(/Version 1 vs Version 2/i)).toBeInTheDocument()
  })

  it('toggles between side-by-side and inline modes', () => {
    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
      />
    )

    const inlineButton = screen.getByRole('button', { name: /inline/i })
    fireEvent.click(inlineButton)

    // Should show unified diff header
    expect(screen.getByText('Unified Diff')).toBeInTheDocument()

    const sideBySideButton = screen.getByRole('button', { name: /side by side/i })
    fireEvent.click(sideBySideButton)

    // Should show original and modified labels (use getAllByText since "Modified" appears in legend too)
    expect(screen.getByText('Original')).toBeInTheDocument()
    const modifiedElements = screen.getAllByText('Modified')
    expect(modifiedElements.length).toBeGreaterThan(0)
  })

  it('swaps sides when swap button is clicked', () => {
    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
        originalLabel="Left"
        modifiedLabel="Right"
      />
    )

    expect(screen.getByText(/Left vs Right/i)).toBeInTheDocument()

    const swapButton = screen.getByLabelText(/swap sides/i)
    fireEvent.click(swapButton)

    expect(screen.getByText(/Right vs Left/i)).toBeInTheDocument()
  })

  it('toggles fullscreen mode', () => {
    const { container } = render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
      />
    )

    const fullscreenButton = screen.getByLabelText(/fullscreen/i)
    const paper = container.querySelector('.MuiPaper-root')

    expect(paper).not.toHaveStyle({ position: 'fixed' })

    fireEvent.click(fullscreenButton)

    expect(paper).toHaveStyle({ position: 'fixed' })

    const exitFullscreenButton = screen.getByLabelText(/exit fullscreen/i)
    fireEvent.click(exitFullscreenButton)

    expect(paper).not.toHaveStyle({ position: 'fixed' })
  })

  it('downloads diff when download button is clicked', () => {
    // Mock URL.createObjectURL and URL.revokeObjectURL
    const mockCreateObjectURL = vi.fn(() => 'blob:mock-url')
    const mockRevokeObjectURL = vi.fn()
    window.URL.createObjectURL = mockCreateObjectURL
    window.URL.revokeObjectURL = mockRevokeObjectURL

    // Mock document.createElement to track link creation
    const mockLink = {
      click: vi.fn(),
      download: '',
      href: '',
    }
    const originalCreateElement = document.createElement.bind(document)
    vi.spyOn(document, 'createElement').mockImplementation((tagName) => {
      if (tagName === 'a') {
        return mockLink as unknown as HTMLAnchorElement
      }
      return originalCreateElement(tagName)
    })

    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
      />
    )

    const downloadButton = screen.getByLabelText(/download diff/i)
    fireEvent.click(downloadButton)

    expect(mockCreateObjectURL).toHaveBeenCalled()
    expect(mockLink.click).toHaveBeenCalled()
    expect(mockLink.download).toMatch(/^diff-\d+\.txt$/)
    expect(mockRevokeObjectURL).toHaveBeenCalledWith('blob:mock-url')
  })

  it('displays legend with diff colors', () => {
    render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
      />
    )

    expect(screen.getByText('Removed')).toBeInTheDocument()
    expect(screen.getByText('Added')).toBeInTheDocument()
    // "Modified" appears in both header and legend, so use getAllByText
    const modifiedElements = screen.getAllByText('Modified')
    expect(modifiedElements.length).toBeGreaterThanOrEqual(1)
  })

  it('supports different languages', () => {
    const { rerender } = render(
      <CodeDiffViewerV2
        originalCode="print('hello')"
        modifiedCode="print('hello world')"
        language="python"
      />
    )

    expect(screen.getByText('Code Comparison')).toBeInTheDocument()

    rerender(
      <CodeDiffViewerV2
        originalCode='{"name": "test"}'
        modifiedCode='{"name": "test", "version": "1.0"}'
        language="json"
      />
    )

    expect(screen.getByText('Code Comparison')).toBeInTheDocument()
  })

  it('supports light and dark themes', () => {
    const { rerender } = render(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
        theme="dark"
      />
    )

    // Check that component renders with dark theme
    expect(screen.getByText('Code Comparison')).toBeInTheDocument()

    rerender(
      <CodeDiffViewerV2
        originalCode={originalCode}
        modifiedCode={modifiedCode}
        language="javascript"
        theme="light"
      />
    )

    // Check that component renders with light theme
    expect(screen.getByText('Code Comparison')).toBeInTheDocument()
  })

  it('handles empty code gracefully', () => {
    render(
      <CodeDiffViewerV2
        originalCode=""
        modifiedCode=""
        language="javascript"
      />
    )

    expect(screen.getByText('Code Comparison')).toBeInTheDocument()
  })

  it('computes diff correctly for inline mode', () => {
    render(
      <CodeDiffViewerV2
        originalCode="line1\nline2\nline3"
        modifiedCode="line1\nline2-modified\nline3\nline4"
        language="text"
      />
    )

    // Switch to inline mode
    const inlineButton = screen.getByRole('button', { name: /inline/i })
    fireEvent.click(inlineButton)

    expect(screen.getByText('Unified Diff')).toBeInTheDocument()
  })
})
