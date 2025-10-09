import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import CodePreviewV2 from '../CodePreviewV2'

describe('Download Button - All File Types', () => {
    let originalCreateElement: typeof document.createElement
    let mockLink: any

    beforeEach(() => {
        // Mock URL.createObjectURL and revokeObjectURL
        globalThis.URL.createObjectURL = vi.fn(() => 'blob:mock-url')
        globalThis.URL.revokeObjectURL = vi.fn()

        // Save original createElement
        originalCreateElement = document.createElement.bind(document)

        // Mock document.createElement for download links
        mockLink = {
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

    const testCases = [
        { language: 'javascript', extension: 'js', code: 'console.log("test");' },
        { language: 'js', extension: 'js', code: 'console.log("test");' },
        { language: 'typescript', extension: 'ts', code: 'const x: number = 5;' },
        { language: 'ts', extension: 'ts', code: 'const x: number = 5;' },
        { language: 'jsx', extension: 'jsx', code: '<div>Hello</div>' },
        { language: 'tsx', extension: 'tsx', code: '<div>Hello</div>' },
        { language: 'python', extension: 'py', code: 'print("hello")' },
        { language: 'py', extension: 'py', code: 'print("hello")' },
        { language: 'json', extension: 'json', code: '{"key": "value"}' },
        { language: 'yaml', extension: 'yaml', code: 'key: value' },
        { language: 'yml', extension: 'yml', code: 'key: value' },
        { language: 'markdown', extension: 'md', code: '# Heading' },
        { language: 'md', extension: 'md', code: '# Heading' },
        { language: 'html', extension: 'html', code: '<html></html>' },
        { language: 'css', extension: 'css', code: 'body { margin: 0; }' },
        { language: 'sql', extension: 'sql', code: 'SELECT * FROM users;' },
        { language: 'shell', extension: 'sh', code: 'echo "test"' },
        { language: 'bash', extension: 'sh', code: 'echo "test"' },
        { language: 'sh', extension: 'sh', code: 'echo "test"' },
        { language: 'unknown', extension: 'txt', code: 'some text' },
    ]

    testCases.forEach(({ language, extension, code }) => {
        it(`should download ${language} files with .${extension} extension`, async () => {
            const user = userEvent.setup()

            render(
                <CodePreviewV2
                    code={code}
                    language={language}
                />
            )

            const downloadButton = screen.getByLabelText('Download')
            await user.click(downloadButton)

            // Verify blob was created
            expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
            const blobCall = (globalThis.URL.createObjectURL as any).mock.calls[0]
            expect(blobCall[0]).toBeInstanceOf(Blob)
            expect(blobCall[0].type).toBe('text/plain')

            // Verify link was created and clicked
            expect(document.createElement).toHaveBeenCalledWith('a')
            expect(mockLink.click).toHaveBeenCalled()
            expect(mockLink.download).toBe(`code.${extension}`)
            expect(mockLink.href).toBe('blob:mock-url')

            // Verify URL was revoked
            expect(globalThis.URL.revokeObjectURL).toHaveBeenCalledWith('blob:mock-url')
        })
    })

    it('should use custom filename when provided', async () => {
        const user = userEvent.setup()

        render(
            <CodePreviewV2
                code="test code"
                language="python"
                filename="my_custom_file.py"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        await user.click(downloadButton)

        expect(mockLink.download).toBe('my_custom_file.py')
    })

    it('should download file with correct content', async () => {
        const user = userEvent.setup()
        const testCode = `def hello():
    print("Hello, World!")
    return True`

        render(
            <CodePreviewV2
                code={testCode}
                language="python"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        await user.click(downloadButton)

        // Verify blob contains correct content
        const blobCall = (globalThis.URL.createObjectURL as any).mock.calls[0]
        const blob = blobCall[0] as Blob

        // Verify blob was created with correct size
        expect(blob.size).toBe(testCode.length)
        expect(blob.type).toBe('text/plain')
    })

    it('should handle empty code', async () => {
        const user = userEvent.setup()

        render(
            <CodePreviewV2
                code=""
                language="javascript"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        await user.click(downloadButton)

        expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
        expect(mockLink.click).toHaveBeenCalled()
    })

    it('should handle very large files', async () => {
        const user = userEvent.setup()
        const largeCode = 'x'.repeat(1000000) // 1MB of text

        render(
            <CodePreviewV2
                code={largeCode}
                language="javascript"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        await user.click(downloadButton)

        expect(globalThis.URL.createObjectURL).toHaveBeenCalled()
        expect(mockLink.click).toHaveBeenCalled()

        // Verify blob size
        const blobCall = (globalThis.URL.createObjectURL as any).mock.calls[0]
        const blob = blobCall[0] as Blob
        expect(blob.size).toBe(largeCode.length)
    })

    it('should handle special characters in code', async () => {
        const user = userEvent.setup()
        const specialCode = `const emoji = "🎉🚀💻";
const unicode = "こんにちは世界";
const symbols = "!@#$%^&*()_+-=[]{}|;':\",./<>?";`

        render(
            <CodePreviewV2
                code={specialCode}
                language="javascript"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        await user.click(downloadButton)

        const blobCall = (globalThis.URL.createObjectURL as any).mock.calls[0]
        const blob = blobCall[0] as Blob
        
        // Verify blob was created successfully
        expect(blob).toBeInstanceOf(Blob)
        expect(blob.type).toBe('text/plain')
        expect(blob.size).toBeGreaterThan(0)
    })

    it('should handle multiple downloads in sequence', async () => {
        const user = userEvent.setup()

        const { rerender } = render(
            <CodePreviewV2
                code="first code"
                language="python"
            />
        )

        const downloadButton = screen.getByLabelText('Download')
        
        // First download
        await user.click(downloadButton)
        expect(mockLink.click).toHaveBeenCalledTimes(1)

        // Second download
        rerender(
            <CodePreviewV2
                code="second code"
                language="javascript"
            />
        )
        await user.click(downloadButton)
        expect(mockLink.click).toHaveBeenCalledTimes(2)

        // Verify URL cleanup
        expect(globalThis.URL.revokeObjectURL).toHaveBeenCalledTimes(2)
    })

    it('should handle case-insensitive language names', async () => {
        const user = userEvent.setup()
        const languages = ['Python', 'PYTHON', 'python', 'PyThOn']

        for (const lang of languages) {
            const { unmount } = render(
                <CodePreviewV2
                    code="test"
                    language={lang}
                />
            )

            const downloadButton = screen.getByLabelText('Download')
            await user.click(downloadButton)

            expect(mockLink.download).toBe('code.py')
            unmount()
        }
    })
})
