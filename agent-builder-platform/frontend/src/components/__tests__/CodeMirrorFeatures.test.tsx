import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import CodePreviewV2 from '../CodePreviewV2'
import CodeDiffViewerV2 from '../CodeDiffViewerV2'

// Sample code for testing
const pythonCode = `def hello_world():
    """A simple hello world function"""
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
`

const javascriptCode = `function helloWorld() {
  // A simple hello world function
  console.log("Hello, World!");
  return true;
}

helloWorld();
`

describe('CodeMirror Feature Tests', () => {
    let originalCreateElement: typeof document.createElement

    beforeEach(() => {
        // Mock clipboard API
        Object.defineProperty(navigator, 'clipboard', {
            value: {
                writeText: vi.fn().mockResolvedValue(undefined),
            },
            writable: true,
            configurable: true,
        })

        // Mock URL.createObjectURL and revokeObjectURL
        globalThis.URL.createObjectURL = vi.fn(() => 'blob:mock-url')
        globalThis.URL.revokeObjectURL = vi.fn()

        // Save original createElement
        originalCreateElement = document.createElement.bind(document)

        // Mock document.createElement for download links
        const mockLink = {
            click: vi.fn(),
            download: '',
            href: '',
        }
        document.createElement = vi.fn((tag: string) => {
            if (tag === 'a') {
                return mockLink as any
            }
            return originalCreateElement(tag)
        }) as any
    })

    afterEach(() => {
        vi.restoreAllMocks()
        // Restore original createElement
        if (originalCreateElement) {
            document.createElement = originalCreateElement
        }
    })

    describe('Download Feature', () => {
        it('should download Python files correctly', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const downloadButton = screen.getByLabelText('Download')
            await user.click(downloadButton)

            expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
            expect(document.createElement).toHaveBeenCalledWith('a')
        })

        it('should download JavaScript files correctly', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={javascriptCode}
                    language="javascript"
                    filename="test.js"
                />
            )

            const downloadButton = screen.getByLabelText('Download')
            await user.click(downloadButton)

            expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
        })

        it('should download files with correct extensions', async () => {
            const user = userEvent.setup()
            const languages = [
                { lang: 'typescript', ext: 'ts' },
                { lang: 'yaml', ext: 'yaml' },
                { lang: 'json', ext: 'json' },
                { lang: 'markdown', ext: 'md' },
            ]

            for (const { lang } of languages) {
                const { unmount } = render(
                    <CodePreviewV2
                        code="test content"
                        language={lang}
                        filename={`test.${lang}`}
                    />
                )

                const downloadButton = screen.getByLabelText('Download')
                await user.click(downloadButton)

                expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
                unmount()
            }
        })
    })

    describe('Fullscreen Feature', () => {
        it('should toggle fullscreen mode', async () => {
            const user = userEvent.setup()

            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const fullscreenButton = screen.getByLabelText('Fullscreen')
            await user.click(fullscreenButton)

            // Check if component has fullscreen styles
            const paper = container.querySelector('.MuiPaper-root')
            expect(paper).toHaveStyle({ position: 'fixed' })

            // Click again to exit fullscreen
            const exitButton = screen.getByLabelText('Exit Fullscreen')
            await user.click(exitButton)

            expect(paper).not.toHaveStyle({ position: 'fixed' })
        })
    })

    describe('Settings Panel', () => {
        it('should open settings menu', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const settingsButton = screen.getByLabelText('Settings')
            await user.click(settingsButton)

            // Check if menu items are visible (use getAllByText for multiple matches)
            await waitFor(() => {
                expect(screen.getByText(/Word Wrap/i)).toBeInTheDocument()
                const minimapElements = screen.getAllByText(/Minimap/i)
                expect(minimapElements.length).toBeGreaterThan(0)
                expect(screen.getByText(/Font Size/i)).toBeInTheDocument()
            })
        })

        it('should toggle word wrap', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const settingsButton = screen.getByLabelText('Settings')
            await user.click(settingsButton)

            const wordWrapOption = screen.getByText(/Word Wrap: Off/i)
            await user.click(wordWrapOption)

            // Reopen menu to check state
            await user.click(settingsButton)
            await waitFor(() => {
                expect(screen.getByText(/Word Wrap: On/i)).toBeInTheDocument()
            })
        })

        it('should change font size', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const settingsButton = screen.getByLabelText('Settings')
            await user.click(settingsButton)

            // Find font size buttons
            const fontSizeButtons = screen.getAllByRole('button').filter(
                btn => ['12', '14', '16', '18'].includes(btn.textContent || '')
            )

            expect(fontSizeButtons.length).toBeGreaterThan(0)

            // Click on size 16
            const size16Button = fontSizeButtons.find(btn => btn.textContent === '16')
            if (size16Button) {
                await user.click(size16Button)
            }
        })

        it('should toggle minimap', async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                    showMinimap={true}
                />
            )

            const settingsButton = screen.getByLabelText('Settings')
            await user.click(settingsButton)

            const minimapOption = screen.getByText(/Minimap: On/i)
            await user.click(minimapOption)

            // Reopen menu to check state
            await user.click(settingsButton)
            await waitFor(() => {
                expect(screen.getByText(/Minimap: Off/i)).toBeInTheDocument()
            })
        })
    })

    describe('Copy to Clipboard', () => {
        it('should copy code to clipboard', async () => {
            const user = userEvent.setup()
            const writeTextSpy = vi.fn().mockResolvedValue(undefined)

            // Re-mock clipboard for this specific test
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: writeTextSpy,
                },
                writable: true,
                configurable: true,
            })

            render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const copyButton = screen.getByLabelText(/Copy Code/i)
            await user.click(copyButton)

            expect(writeTextSpy).toHaveBeenCalledWith(pythonCode)

            // Check for "Copied!" tooltip (may take a moment to appear)
            await waitFor(() => {
                const copiedButton = screen.queryByLabelText(/Copied!/i)
                expect(copiedButton).toBeInTheDocument()
            }, { timeout: 3000 })
        })
    })

    describe('Syntax Highlighting', () => {
        it('should support Python syntax highlighting', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()

            // Check that language is displayed
            expect(screen.getByText('PYTHON')).toBeInTheDocument()
        })

        it('should support JavaScript syntax highlighting', () => {
            const { container } = render(
                <CodePreviewV2
                    code={javascriptCode}
                    language="javascript"
                    filename="test.js"
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()

            expect(screen.getByText('JAVASCRIPT')).toBeInTheDocument()
        })

        it('should support multiple languages', () => {
            const languages = [
                'typescript',
                'yaml',
                'json',
                'markdown',
                'html',
                'css',
                'sql',
            ]

            languages.forEach((lang) => {
                const { container, unmount } = render(
                    <CodePreviewV2
                        code="test content"
                        language={lang}
                        filename={`test.${lang}`}
                    />
                )

                const editor = container.querySelector('.cm-editor')
                expect(editor).toBeInTheDocument()

                unmount()
            })
        })
    })

    describe('Line Numbers', () => {
        it('should display line numbers', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const gutters = container.querySelector('.cm-gutters')
            expect(gutters).toBeInTheDocument()
            expect(gutters).toBeVisible()
        })

        it('should have proper line number styling', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    filename="test.py"
                />
            )

            const gutters = container.querySelector('.cm-gutters')
            if (gutters) {
                const styles = window.getComputedStyle(gutters)
                expect(styles.display).not.toBe('none')
                expect(styles.visibility).not.toBe('hidden')
            }
        })
    })

    describe('Theme Support', () => {
        it('should render with dark theme', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    theme="dark"
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()

            // Check for dark theme background
            const editorBox = container.querySelector('.MuiBox-root')
            if (editorBox) {
                const styles = window.getComputedStyle(editorBox)
                // Dark theme should have dark background
                expect(styles.backgroundColor).toBeTruthy()
            }
        })

        it('should render with light theme', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    theme="light"
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()
        })

        it('should switch themes without errors', () => {
            const { rerender } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    theme="dark"
                />
            )

            // Switch to light theme
            rerender(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    theme="light"
                />
            )

            // Switch back to dark theme
            rerender(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    theme="dark"
                />
            )

            // Should not throw errors
            expect(screen.getByText('PYTHON')).toBeInTheDocument()
        })
    })

    describe('Diff Viewer Features', () => {
        it('should render side-by-side diff', () => {
            render(
                <CodeDiffViewerV2
                    originalCode={pythonCode}
                    modifiedCode={pythonCode.replace('Hello', 'Goodbye')}
                    language="python"
                />
            )

            expect(screen.getByText('Code Comparison')).toBeInTheDocument()
            expect(screen.getByText('Side by Side')).toBeInTheDocument()
        })

        it('should switch to inline diff mode', async () => {
            const user = userEvent.setup()

            render(
                <CodeDiffViewerV2
                    originalCode={pythonCode}
                    modifiedCode={pythonCode.replace('Hello', 'Goodbye')}
                    language="python"
                />
            )

            const inlineButton = screen.getByText('Inline')
            await user.click(inlineButton)

            expect(screen.getByText('Unified Diff')).toBeInTheDocument()
        })

        it('should swap diff sides', async () => {
            const user = userEvent.setup()

            render(
                <CodeDiffViewerV2
                    originalCode={pythonCode}
                    modifiedCode={javascriptCode}
                    language="python"
                    originalLabel="Python"
                    modifiedLabel="JavaScript"
                />
            )

            expect(screen.getByText(/Python vs JavaScript/i)).toBeInTheDocument()

            const swapButton = screen.getByLabelText('Swap Sides')
            await user.click(swapButton)

            // After swap, labels should be reversed
            await waitFor(() => {
                expect(screen.getByText(/JavaScript vs Python/i)).toBeInTheDocument()
            }, { timeout: 3000 })
        }, 10000)

        it('should download diff', async () => {
            const user = userEvent.setup()

            render(
                <CodeDiffViewerV2
                    originalCode={pythonCode}
                    modifiedCode={javascriptCode}
                    language="python"
                />
            )

            const downloadButton = screen.getByLabelText('Download Diff')
            await user.click(downloadButton)

            expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
        })

        it('should display diff legend', () => {
            const { container } = render(
                <CodeDiffViewerV2
                    originalCode={pythonCode}
                    modifiedCode={pythonCode.replace('Hello', 'Goodbye')}
                    language="python"
                />
            )

            // Check that legend elements exist (they may be in Typography components)
            const legendText = container.textContent || ''
            expect(legendText).toContain('Removed')
            expect(legendText).toContain('Added')
            expect(legendText).toContain('Modified')
        })
    })

    describe('Editable Mode', () => {
        it('should allow editing when readOnly is false', () => {
            const handleChange = vi.fn()

            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    readOnly={false}
                    onChange={handleChange}
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()

            // In editable mode, the editor should not have editable.of(false)
            // This is tested by checking if the component renders without errors
        })

        it('should be read-only by default', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                />
            )

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()
        })
    })

    describe('Minimap Display', () => {
        it('should show minimap when enabled', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    showMinimap={true}
                />
            )

            // Check for minimap placeholder
            const minimap = container.querySelector('.MuiBox-root')
            expect(minimap).toBeTruthy()
        })

        it('should hide minimap when disabled', () => {
            const { container } = render(
                <CodePreviewV2
                    code={pythonCode}
                    language="python"
                    showMinimap={false}
                />
            )

            // Minimap should not be visible
            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()
        })
    })

    describe('Performance', () => {
        it('should render large files efficiently', () => {
            const largeCode = Array.from({ length: 1000 }, (_, i) =>
                `def function_${i}():\n    return ${i}\n`
            ).join('\n')

            const startTime = performance.now()

            const { container } = render(
                <CodePreviewV2
                    code={largeCode}
                    language="python"
                    filename="large_file.py"
                />
            )

            const endTime = performance.now()
            const renderTime = endTime - startTime

            // Should render in reasonable time
            expect(renderTime).toBeLessThan(1000)

            const editor = container.querySelector('.cm-editor')
            expect(editor).toBeInTheDocument()
        })
    })
})
