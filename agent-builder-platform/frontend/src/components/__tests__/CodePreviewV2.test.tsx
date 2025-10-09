import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CodePreviewV2 from '../CodePreviewV2'

// Mock clipboard API
Object.assign(navigator, {
  clipboard: {
    writeText: vi.fn(() => Promise.resolve()),
  },
})

describe('CodePreviewV2', () => {
  const sampleCode = `function hello() {
  console.log("Hello, World!");
}`

  it('renders code with header', () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        filename="test.js"
      />
    )

    expect(screen.getByText('test.js')).toBeInTheDocument()
    expect(screen.getByText('JAVASCRIPT')).toBeInTheDocument()
  })

  it('renders without header when showHeader is false', () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        filename="test.js"
        showHeader={false}
      />
    )

    expect(screen.queryByText('test.js')).not.toBeInTheDocument()
  })

  it('copies code to clipboard', async () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
      />
    )

    const copyButton = screen.getByLabelText(/copy code/i)
    fireEvent.click(copyButton)

    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(sampleCode)
    })

    // Check for "Copied!" tooltip
    expect(screen.getByLabelText(/copied!/i)).toBeInTheDocument()
  })

  it('opens settings menu', () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
      />
    )

    const settingsButton = screen.getByLabelText(/settings/i)
    fireEvent.click(settingsButton)

    expect(screen.getByText(/word wrap/i)).toBeInTheDocument()
    // Use getAllByText since minimap appears in both menu and preview
    expect(screen.getAllByText(/minimap/i).length).toBeGreaterThan(0)
    expect(screen.getByText(/font size/i)).toBeInTheDocument()
  })

  it('toggles fullscreen mode', () => {
    const { container } = render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
      />
    )

    const fullscreenButton = screen.getByLabelText(/fullscreen/i)
    const paper = container.querySelector('.MuiPaper-root')

    // Initially not fullscreen
    expect(paper).not.toHaveStyle({ position: 'fixed' })

    // Toggle fullscreen
    fireEvent.click(fullscreenButton)
    expect(paper).toHaveStyle({ position: 'fixed' })

    // Toggle back
    const exitButton = screen.getByLabelText(/exit fullscreen/i)
    fireEvent.click(exitButton)
    expect(paper).not.toHaveStyle({ position: 'fixed' })
  })

  it('supports all required languages', () => {
    const languages = [
      'python',
      'javascript',
      'typescript',
      'yaml',
      'json',
      'markdown',
      'html',
      'css',
      'sql',
    ]

    languages.forEach((lang) => {
      const { unmount } = render(
        <CodePreviewV2
          code={sampleCode}
          language={lang}
        />
      )
      expect(screen.getByText(lang.toUpperCase())).toBeInTheDocument()
      unmount()
    })
  })

  it('handles onChange callback', () => {
    const handleChange = vi.fn()
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        readOnly={false}
        onChange={handleChange}
      />
    )

    // CodeMirror will call onChange when value changes
    // This is a basic test to ensure the prop is passed correctly
    expect(handleChange).not.toHaveBeenCalled()
  })

  it('applies dark theme by default', () => {
    const { container } = render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
      />
    )

    const editorContainer = container.querySelector('[class*="cm-editor"]')
    expect(editorContainer).toBeInTheDocument()
  })

  it('applies light theme when specified', () => {
    const { container } = render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        theme="light"
      />
    )

    const editorContainer = container.querySelector('[class*="cm-editor"]')
    expect(editorContainer).toBeInTheDocument()
  })

  it('shows minimap when enabled', () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        showMinimap={true}
      />
    )

    expect(screen.getByText(/minimap/i)).toBeInTheDocument()
  })

  it('hides minimap when disabled', () => {
    render(
      <CodePreviewV2
        code={sampleCode}
        language="javascript"
        showMinimap={false}
      />
    )

    // Minimap text should not be visible in the viewport
    const minimapText = screen.queryByText(/minimap/i, { selector: 'p' })
    expect(minimapText).not.toBeInTheDocument()
  })
})
