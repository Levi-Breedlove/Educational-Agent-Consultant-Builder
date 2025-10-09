import { useState } from 'react'
import { Box, Container, Typography, Paper, Tabs, Tab, Button, Stack } from '@mui/material'
import CodePreviewV2 from '../components/CodePreviewV2'
import CodeDiffViewerV2 from '../components/CodeDiffViewerV2'
import CodeWorkspace from '../components/CodeWorkspace'

const pythonCode = `def hello_world():
    """A simple hello world function"""
    print("Hello, World!")
    return True

def calculate_sum(a, b):
    """Calculate the sum of two numbers"""
    result = a + b
    print(f"The sum of {a} and {b} is {result}")
    return result

if __name__ == "__main__":
    hello_world()
    calculate_sum(5, 10)
`

const javascriptCode = `function helloWorld() {
  // A simple hello world function
  console.log("Hello, World!");
  return true;
}

function calculateSum(a, b) {
  // Calculate the sum of two numbers
  const result = a + b;
  console.log(\`The sum of \${a} and \${b} is \${result}\`);
  return result;
}

helloWorld();
calculateSum(5, 10);
`

const typescriptCode = `interface Person {
  name: string;
  age: number;
}

function greet(person: Person): string {
  return \`Hello, \${person.name}! You are \${person.age} years old.\`;
}

const user: Person = {
  name: "Alice",
  age: 30
};

console.log(greet(user));
`

const yamlCode = `# Configuration file
server:
  host: localhost
  port: 8080
  ssl: true

database:
  host: db.example.com
  port: 5432
  name: myapp
  user: admin
  password: secret123

features:
  - authentication
  - logging
  - monitoring
`

const sampleFiles = [
  { path: 'src/main.py', content: pythonCode, language: 'python' },
  { path: 'src/app.js', content: javascriptCode, language: 'javascript' },
  { path: 'src/types.ts', content: typescriptCode, language: 'typescript' },
  { path: 'config/settings.yaml', content: yamlCode, language: 'yaml' },
]

type TabValue = 'preview' | 'diff' | 'workspace' | 'editable'

export default function CodeMirrorTestPage() {
  const [activeTab, setActiveTab] = useState<TabValue>('preview')
  const [theme, setTheme] = useState<'dark' | 'light'>('dark')

  const handleTabChange = (_: React.SyntheticEvent, newValue: TabValue) => {
    setActiveTab(newValue)
  }

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h4" component="h1">
            CodeMirror 6 Feature Test Page
          </Typography>
          <Button variant="contained" onClick={toggleTheme}>
            Toggle Theme ({theme})
          </Button>
        </Stack>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          This page demonstrates all CodeMirror 6 features. Test each tab to verify:
        </Typography>
        
        <Box component="ul" sx={{ pl: 3 }}>
          <li>✅ Edit/Lock button - Toggle between read-only and editable modes</li>
          <li>✅ Save button - Save changes (appears when editing)</li>
          <li>✅ Download button (top-right, download icon)</li>
          <li>✅ Copy button (top-right, copy icon)</li>
          <li>✅ Fullscreen button (top-right, fullscreen icon)</li>
          <li>✅ Settings button (top-right, gear icon)</li>
          <li>✅ Settings menu with Word Wrap, Minimap, Theme, Font Size toggles</li>
          <li>✅ Line numbers visible in left gutter</li>
          <li>✅ Syntax highlighting for all languages</li>
          <li>✅ Working minimap on the right side (updates as you type)</li>
          <li>✅ Diff viewer with side-by-side and inline modes</li>
          <li>✅ Editable mode (type in the code box)</li>
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 2 }}>
        <Tabs value={activeTab} onChange={handleTabChange} sx={{ mb: 2 }}>
          <Tab label="Code Preview" value="preview" />
          <Tab label="Diff Viewer" value="diff" />
          <Tab label="Code Workspace" value="workspace" />
          <Tab label="Editable Mode" value="editable" />
        </Tabs>

        <Box sx={{ minHeight: 600 }}>
          {activeTab === 'preview' && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Code Preview - Python Example
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Test: Click Edit button to enable editing, make changes, then click Save. 
                Also test Download, Copy, Fullscreen, and Settings buttons. Check the minimap on the right side.
              </Typography>
              <CodePreviewV2
                code={pythonCode}
                language="python"
                filename="hello_world.py"
                theme={theme}
                showHeader={true}
                showMinimap={true}
                enableEdit={true}
                readOnly={false}
                onSave={(value) => {
                  console.log('Saved:', value.length, 'characters')
                  alert('File saved successfully!')
                }}
              />
            </Box>
          )}

          {activeTab === 'diff' && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Diff Viewer - Python vs JavaScript
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Test: Toggle between Side-by-Side and Inline modes. Click Swap Sides and Download Diff buttons.
              </Typography>
              <CodeDiffViewerV2
                originalCode={pythonCode}
                modifiedCode={javascriptCode}
                language="python"
                originalLabel="Python Version"
                modifiedLabel="JavaScript Version"
                theme={theme}
              />
            </Box>
          )}

          {activeTab === 'workspace' && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Code Workspace - Multiple Files
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Test: Select files from the tree. Each file should show Download, Copy, Fullscreen, and Settings buttons.
              </Typography>
              <Box sx={{ height: 600 }}>
                <CodeWorkspace
                  files={sampleFiles}
                  title="Sample Project Files"
                />
              </Box>
            </Box>
          )}

          {activeTab === 'editable' && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Editable Mode - TypeScript Example
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Test: Click Edit button to unlock, then type in the editor. Click Save to save changes.
                Watch the minimap update as you type. All buttons should be visible and functional.
              </Typography>
              <CodePreviewV2
                code={typescriptCode}
                language="typescript"
                filename="types.ts"
                theme={theme}
                readOnly={false}
                enableEdit={true}
                showHeader={true}
                showMinimap={true}
                onChange={(value) => console.log('Code changed:', value.length, 'characters')}
                onSave={(value) => {
                  console.log('Saved:', value.length, 'characters')
                  alert('TypeScript file saved!')
                }}
              />
            </Box>
          )}
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Testing Checklist
        </Typography>
        
        <Box component="ul" sx={{ pl: 3 }}>
          <li>
            <strong>Edit/Lock Button:</strong> Click the Edit icon (✏️) to enable editing. 
            Icon changes to Lock (🔒) when in edit mode. Click again to lock (read-only).
          </li>
          <li>
            <strong>Save Button:</strong> Make changes to the code, then click Save icon (💾). 
            Button is disabled when no changes. Success message appears after saving.
          </li>
          <li>
            <strong>Download Button:</strong> Click the download icon (⬇️) in the top-right corner. 
            File should download with correct extension (.py, .js, .ts, .yaml).
          </li>
          <li>
            <strong>Copy Button:</strong> Click the copy icon (📋) in the top-right corner. 
            Tooltip should change to "Copied!" and code should be in clipboard.
          </li>
          <li>
            <strong>Fullscreen Button:</strong> Click the fullscreen icon (⛶) in the top-right corner. 
            Editor should expand to full screen. Click again to exit.
          </li>
          <li>
            <strong>Settings Button:</strong> Click the gear icon (⚙️) in the top-right corner. 
            Menu should open with Word Wrap, Minimap, Theme, and Font Size options.
          </li>
          <li>
            <strong>Word Wrap Toggle:</strong> In Settings menu, click "Word Wrap: Off". 
            Long lines should wrap. Click again to turn off.
          </li>
          <li>
            <strong>Minimap:</strong> Look at the right side of the editor. 
            You should see a minimap showing an overview of the code. It updates as you type.
          </li>
          <li>
            <strong>Minimap Toggle:</strong> In Settings menu, click "Minimap: On/Off". 
            Minimap should appear/disappear on the right side.
          </li>
          <li>
            <strong>Font Size Buttons:</strong> In Settings menu, click 12, 14, 16, or 18. 
            Text size should change immediately.
          </li>
          <li>
            <strong>Line Numbers:</strong> Look at the left gutter. 
            Line numbers (1, 2, 3...) should be clearly visible.
          </li>
          <li>
            <strong>Syntax Highlighting:</strong> Keywords, strings, and comments should be colored differently.
          </li>
          <li>
            <strong>Editable Mode:</strong> Go to "Editable Mode" tab, click Edit button, then type in the editor. 
            Text should appear with syntax highlighting. Minimap should update in real-time.
          </li>
        </Box>
      </Paper>
    </Container>
  )
}
