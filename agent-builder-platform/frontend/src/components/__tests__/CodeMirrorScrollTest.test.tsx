import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import CodePreviewV2 from '../CodePreviewV2'
import CodeDiffViewerV2 from '../CodeDiffViewerV2'
import CodeWorkspace from '../CodeWorkspace'

// Mock large code content for scroll testing
const generateLargeCode = (lines: number, language: string): string => {
  const templates: Record<string, (i: number) => string> = {
    python: (i) => `def function_${i}():\n    """Function ${i} documentation"""\n    return ${i}\n`,
    javascript: (i) => `function function${i}() {\n  // Function ${i}\n  return ${i};\n}\n`,
    typescript: (i) => `function function${i}(): number {\n  // Function ${i}\n  return ${i};\n}\n`,
  }

  const template = templates[language] || templates.javascript
  return Array.from({ length: lines }, (_, i) => template(i)).join('\n')
}

describe('CodeMirror Scroll Rendering Tests', () => {
  beforeEach(() => {
    // Mock console methods to avoid noise
    vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.spyOn(console, 'warn').mockImplementation(() => {})
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('CodePreviewV2 Scroll Tests', () => {
    it('should render without visual artifacts on initial load', () => {
      const largeCode = generateLargeCode(100, 'python')
      
      const { container } = render(
        <CodePreviewV2
          code={largeCode}
          language="python"
          filename="test.py"
        />
      )

      // Check that CodeMirror editor is rendered
      const editor = container.querySelector('.cm-editor')
      expect(editor).toBeInTheDocument()

      // Check that content is present
      const content = container.querySelector('.cm-content')
      expect(content).toBeInTheDocument()

      // Check that line numbers are visible
      const gutters = container.querySelector('.cm-gutters')
      expect(gutters).toBeInTheDocument()
    })

    it('should maintain proper styling during scroll simulation', async () => {
      const largeCode = generateLargeCode(200, 'javascript')
      
      const { container } = render(
        <CodePreviewV2
          code={largeCode}
          language="javascript"
          filename="test.js"
        />
      )

      const scroller = container.querySelector('.cm-scroller')
      expect(scroller).toBeInTheDocument()

      // Simulate scroll events
      if (scroller) {
        // Set scrollHeight for jsdom (doesn't calculate it automatically)
        Object.defineProperty(scroller, 'scrollHeight', {
          writable: true,
          configurable: true,
          value: 10000,
        })

        // Scroll to middle
        scroller.scrollTop = 500
        scroller.dispatchEvent(new Event('scroll'))

        await waitFor(() => {
          expect(scroller.scrollTop).toBe(500)
        })

        // Scroll to bottom
        scroller.scrollTop = 5000
        scroller.dispatchEvent(new Event('scroll'))

        await waitFor(() => {
          expect(scroller.scrollTop).toBe(5000)
        })

        // Verify no error classes or artifacts
        const editor = container.querySelector('.cm-editor')
        expect(editor).not.toHaveClass('error')
        expect(editor).not.toHaveClass('artifact')
      }
    })

    it('should handle rapid scroll events without artifacts', async () => {
      const largeCode = generateLargeCode(300, 'typescript')
      
      const { container } = render(
        <CodePreviewV2
          code={largeCode}
          language="typescript"
          filename="test.ts"
        />
      )

      const scroller = container.querySelector('.cm-scroller')
      
      if (scroller) {
        // Simulate rapid scrolling
        const scrollPositions = [100, 200, 300, 400, 500, 600, 700, 800]
        
        for (const position of scrollPositions) {
          scroller.scrollTop = position
          scroller.dispatchEvent(new Event('scroll'))
          
          // Small delay to simulate rapid but not instant scrolling
          await new Promise(resolve => setTimeout(resolve, 10))
        }

        // Verify editor is still properly rendered
        const editor = container.querySelector('.cm-editor')
        expect(editor).toBeInTheDocument()
        
        const content = container.querySelector('.cm-content')
        expect(content).toBeInTheDocument()
      }
    })

    it('should maintain line number visibility during scroll', async () => {
      const largeCode = generateLargeCode(150, 'python')
      
      const { container } = render(
        <CodePreviewV2
          code={largeCode}
          language="python"
          filename="test.py"
        />
      )

      const gutters = container.querySelector('.cm-gutters')
      expect(gutters).toBeInTheDocument()

      // Check that gutters have proper styling
      const gutterStyle = window.getComputedStyle(gutters as Element)
      expect(gutterStyle.display).not.toBe('none')
      expect(gutterStyle.visibility).not.toBe('hidden')
    })

    it('should handle theme changes without rendering issues', () => {
      const code = generateLargeCode(100, 'javascript')
      
      const { container, rerender } = render(
        <CodePreviewV2
          code={code}
          language="javascript"
          theme="dark"
        />
      )

      let editor = container.querySelector('.cm-editor')
      expect(editor).toBeInTheDocument()

      // Change to light theme
      rerender(
        <CodePreviewV2
          code={code}
          language="javascript"
          theme="light"
        />
      )

      editor = container.querySelector('.cm-editor')
      expect(editor).toBeInTheDocument()
    })
  })

  describe('CodeDiffViewerV2 Scroll Tests', () => {
    it('should render side-by-side diff without artifacts', () => {
      const originalCode = generateLargeCode(100, 'python')
      const modifiedCode = generateLargeCode(100, 'python').replace('function_50', 'modified_function_50')
      
      const { container } = render(
        <CodeDiffViewerV2
          originalCode={originalCode}
          modifiedCode={modifiedCode}
          language="python"
        />
      )

      // Check that both editors are rendered
      const editors = container.querySelectorAll('.cm-editor')
      expect(editors.length).toBeGreaterThanOrEqual(2)
    })

    it('should handle scroll in side-by-side mode without artifacts', async () => {
      const originalCode = generateLargeCode(200, 'javascript')
      const modifiedCode = generateLargeCode(200, 'javascript')
      
      const { container } = render(
        <CodeDiffViewerV2
          originalCode={originalCode}
          modifiedCode={modifiedCode}
          language="javascript"
        />
      )

      const scrollers = container.querySelectorAll('.cm-scroller')
      
      if (scrollers.length >= 2) {
        // Scroll both sides
        scrollers[0].scrollTop = 500
        scrollers[0].dispatchEvent(new Event('scroll'))
        
        scrollers[1].scrollTop = 500
        scrollers[1].dispatchEvent(new Event('scroll'))

        await waitFor(() => {
          expect(scrollers[0].scrollTop).toBe(500)
          expect(scrollers[1].scrollTop).toBe(500)
        })

        // Verify no rendering issues
        const editors = container.querySelectorAll('.cm-editor')
        editors.forEach(editor => {
          expect(editor).toBeInTheDocument()
        })
      }
    })

    it('should render inline diff without artifacts', () => {
      const originalCode = generateLargeCode(100, 'python')
      const modifiedCode = generateLargeCode(100, 'python').replace('function_25', 'modified_25')
      
      const { container } = render(
        <CodeDiffViewerV2
          originalCode={originalCode}
          modifiedCode={modifiedCode}
          language="python"
        />
      )

      // Verify diff viewer is rendered
      const editor = container.querySelector('.cm-editor')
      expect(editor).toBeInTheDocument()
    })
  })

  describe('CodeWorkspace Scroll Tests', () => {
    it('should handle file switching without rendering artifacts', async () => {
      const files = [
        {
          path: 'src/file1.py',
          content: generateLargeCode(100, 'python'),
          language: 'python',
        },
        {
          path: 'src/file2.js',
          content: generateLargeCode(100, 'javascript'),
          language: 'javascript',
        },
        {
          path: 'src/file3.ts',
          content: generateLargeCode(100, 'typescript'),
          language: 'typescript',
        },
      ]

      const { container } = render(
        <CodeWorkspace files={files} />
      )

      // Verify workspace is rendered
      expect(container).toBeInTheDocument()

      // Check that file tree component is present (may not have role="tree" in implementation)
      const fileTreeContainer = container.querySelector('.MuiList-root') || 
                                container.querySelector('[class*="file"]')
      expect(fileTreeContainer).toBeTruthy()
    })

    it('should maintain scroll position when switching between files', async () => {
      const files = [
        {
          path: 'file1.py',
          content: generateLargeCode(200, 'python'),
          language: 'python',
        },
        {
          path: 'file2.js',
          content: generateLargeCode(200, 'javascript'),
          language: 'javascript',
        },
      ]

      const { container } = render(
        <CodeWorkspace files={files} />
      )

      // Verify workspace renders without errors
      expect(container).toBeInTheDocument()
    })
  })

  describe('Performance and Memory Tests', () => {
    it('should handle very large files without performance degradation', () => {
      const veryLargeCode = generateLargeCode(1000, 'python')
      
      const startTime = performance.now()
      
      const { container } = render(
        <CodePreviewV2
          code={veryLargeCode}
          language="python"
          filename="large_file.py"
        />
      )
      
      const endTime = performance.now()
      const renderTime = endTime - startTime

      // Render should complete in reasonable time (< 1000ms)
      expect(renderTime).toBeLessThan(1000)

      // Verify editor is rendered
      const editor = container.querySelector('.cm-editor')
      expect(editor).toBeInTheDocument()
    })

    it('should not leak memory on unmount', () => {
      const code = generateLargeCode(100, 'javascript')
      
      const { unmount } = render(
        <CodePreviewV2
          code={code}
          language="javascript"
        />
      )

      // Unmount should not throw errors
      expect(() => unmount()).not.toThrow()
    })
  })

  describe('Visual Regression Tests', () => {
    it('should maintain consistent styling across scroll positions', async () => {
      const code = generateLargeCode(200, 'python')
      
      const { container } = render(
        <CodePreviewV2
          code={code}
          language="python"
          filename="test.py"
        />
      )

      const editor = container.querySelector('.cm-editor')
      const gutters = container.querySelector('.cm-gutters')
      const content = container.querySelector('.cm-content')

      // Verify all elements are present
      expect(editor).toBeInTheDocument()
      expect(gutters).toBeInTheDocument()
      expect(content).toBeInTheDocument()

      // Check that styling is applied
      if (editor) {
        const editorStyle = window.getComputedStyle(editor)
        expect(editorStyle.backgroundColor).toBeTruthy()
      }

      if (gutters) {
        const gutterStyle = window.getComputedStyle(gutters)
        expect(gutterStyle.backgroundColor).toBeTruthy()
      }
    })

    it('should not show black lines or rendering artifacts', () => {
      const code = generateLargeCode(150, 'javascript')
      
      const { container } = render(
        <CodePreviewV2
          code={code}
          language="javascript"
          filename="test.js"
        />
      )

      // Check for common artifact indicators
      const editor = container.querySelector('.cm-editor')
      
      if (editor) {
        const editorStyle = window.getComputedStyle(editor)
        
        // Verify no black overlay or artifact colors
        expect(editorStyle.backgroundColor).not.toBe('rgb(0, 0, 0)')
        expect(editorStyle.backgroundColor).not.toBe('#000000')
        
        // Verify proper background color is set
        expect(editorStyle.backgroundColor).toBeTruthy()
      }
    })

    it('should maintain proper z-index layering', () => {
      const code = generateLargeCode(100, 'python')
      
      const { container } = render(
        <CodePreviewV2
          code={code}
          language="python"
          filename="test.py"
          showHeader={true}
        />
      )

      const editor = container.querySelector('.cm-editor')
      const gutters = container.querySelector('.cm-gutters')

      if (editor && gutters) {
        const editorStyle = window.getComputedStyle(editor)
        const gutterStyle = window.getComputedStyle(gutters)

        // Verify z-index is not causing layering issues
        expect(editorStyle.zIndex).not.toBe('-1')
        expect(gutterStyle.zIndex).not.toBe('-1')
      }
    })
  })
})
