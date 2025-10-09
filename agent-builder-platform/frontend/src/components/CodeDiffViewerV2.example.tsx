/**
 * CodeDiffViewerV2 Usage Examples
 * 
 * This file demonstrates how to use the CodeDiffViewerV2 component
 * with CodeMirror 6 for displaying code differences.
 */

import CodeDiffViewerV2 from './CodeDiffViewerV2'

// Example 1: Basic usage with JavaScript
export function BasicJavaScriptDiff() {
  const originalCode = `function hello() {
  console.log('Hello');
  return true;
}`

  const modifiedCode = `function hello() {
  console.log('Hello World');
  console.log('Modified');
  return true;
}`

  return (
    <CodeDiffViewerV2
      originalCode={originalCode}
      modifiedCode={modifiedCode}
      language="javascript"
    />
  )
}

// Example 2: Python diff with custom labels
export function PythonDiffWithLabels() {
  const originalCode = `def calculate(x, y):
    result = x + y
    return result`

  const modifiedCode = `def calculate(x, y):
    # Added validation
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Arguments must be numbers")
    result = x + y
    return result`

  return (
    <CodeDiffViewerV2
      originalCode={originalCode}
      modifiedCode={modifiedCode}
      language="python"
      originalLabel="Version 1.0"
      modifiedLabel="Version 2.0"
    />
  )
}

// Example 3: JSON diff with light theme
export function JSONDiffLightTheme() {
  const originalCode = `{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0"
  }
}`

  const modifiedCode = `{
  "name": "my-app",
  "version": "2.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}`

  return (
    <CodeDiffViewerV2
      originalCode={originalCode}
      modifiedCode={modifiedCode}
      language="json"
      theme="light"
    />
  )
}

// Example 4: YAML configuration diff
export function YAMLConfigDiff() {
  const originalCode = `version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"`

  const modifiedCode = `version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production`

  return (
    <CodeDiffViewerV2
      originalCode={originalCode}
      modifiedCode={modifiedCode}
      language="yaml"
      originalLabel="Development"
      modifiedLabel="Production"
    />
  )
}

// Example 5: TypeScript diff
export function TypeScriptDiff() {
  const originalCode = `interface User {
  id: number;
  name: string;
}

function getUser(id: number): User {
  return { id, name: 'John' };
}`

  const modifiedCode = `interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

function getUser(id: number): Promise<User> {
  return fetch(\`/api/users/\${id}\`)
    .then(res => res.json());
}`

  return (
    <CodeDiffViewerV2
      originalCode={originalCode}
      modifiedCode={modifiedCode}
      language="typescript"
      originalLabel="Before Refactor"
      modifiedLabel="After Refactor"
    />
  )
}

/**
 * Features:
 * 
 * 1. Side-by-side and inline diff modes
 *    - Toggle between viewing diffs side-by-side or in a unified view
 * 
 * 2. Swap sides functionality
 *    - Quickly swap which code appears on left vs right
 * 
 * 3. Download diff
 *    - Export the diff as a text file
 * 
 * 4. Legend for diff colors
 *    - Visual legend showing removed (red), added (green), and modified (yellow) lines
 * 
 * 5. Fullscreen mode
 *    - Expand the diff viewer to full screen for better visibility
 * 
 * 6. Syntax highlighting
 *    - Supports JavaScript, TypeScript, Python, JSON, YAML, HTML, CSS, SQL, and more
 * 
 * 7. Light and dark themes
 *    - Matches your application's theme
 * 
 * 8. No GPU rendering artifacts
 *    - Uses CodeMirror 6 instead of Monaco to avoid Chrome GPU compositing bugs
 */
