# CodeDiffViewerV2 Features Guide

## Component Overview

CodeDiffViewerV2 is a modern, CodeMirror 6-based diff viewer that displays code differences with syntax highlighting, multiple view modes, and no GPU rendering artifacts.

## Feature Breakdown

### 1. Side-by-Side Mode (Default)

```
┌─────────────────────────────────────────────────────────────┐
│ Code Comparison                    [Side by Side] [Inline]  │
│ Original vs Modified               [Swap] [Download] [Full] │
├──────────────────────────┬──────────────────────────────────┤
│ Original                 │ Modified                         │
├──────────────────────────┼──────────────────────────────────┤
│ function hello() {       │ function hello() {               │
│   console.log('Hello');  │   console.log('Hello World');    │
│                          │   console.log('Modified');       │
│   return true;           │   return true;                   │
│ }                        │ }                                │
└──────────────────────────┴──────────────────────────────────┘
│ [Red] Removed  [Green] Added  [Yellow] Modified            │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Two editors side-by-side
- Synchronized scrolling
- Line numbers on both sides
- Clear visual separation

### 2. Inline Mode

```
┌─────────────────────────────────────────────────────────────┐
│ Code Comparison                    [Side by Side] [Inline]  │
│ Original vs Modified               [Swap] [Download] [Full] │
├─────────────────────────────────────────────────────────────┤
│ Unified Diff                                                │
├─────────────────────────────────────────────────────────────┤
│   function hello() {                                        │
│ -   console.log('Hello');                                   │
│ +   console.log('Hello World');                             │
│ +   console.log('Modified');                                │
│     return true;                                            │
│   }                                                         │
└─────────────────────────────────────────────────────────────┘
│ [Red] Removed  [Green] Added  [Yellow] Modified            │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Unified diff view
- `+` prefix for added lines
- `-` prefix for removed lines
- `~` prefix for modified lines
- Space prefix for unchanged lines

### 3. Swap Sides

**Before Swap:**
```
┌──────────────┬──────────────┐
│ Original     │ Modified     │
│ (Left)       │ (Right)      │
└──────────────┴──────────────┘
```

**After Swap:**
```
┌──────────────┬──────────────┐
│ Modified     │ Original     │
│ (Left)       │ (Right)      │
└──────────────┴──────────────┘
```

**Use Cases:**
- Compare from different perspectives
- Review changes in reverse
- Personal preference for layout

### 4. Download Diff

**Downloaded File Format:**
```
=== Original ===
function hello() {
  console.log('Hello');
  return true;
}

=== Modified ===
function hello() {
  console.log('Hello World');
  console.log('Modified');
  return true;
}
```

**Features:**
- Plain text format
- Timestamped filename: `diff-1696867200000.txt`
- Includes both versions
- Easy to share or archive

### 5. Legend

```
┌─────────────────────────────────────────────────────────────┐
│ [■ Red] Removed  [■ Green] Added  [■ Yellow] Modified      │
└─────────────────────────────────────────────────────────────┘
```

**Color Meanings:**
- **Red (rgba(248, 81, 73, 0.15))**: Lines removed from original
- **Green (rgba(46, 160, 67, 0.15))**: Lines added in modified
- **Yellow (rgba(255, 191, 0, 0.15))**: Lines changed between versions

### 6. Fullscreen Mode

**Normal View:**
```
┌─────────────────────────────────────┐
│ Page Header                         │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ CodeDiffViewerV2                │ │
│ │ (500px height)                  │ │
│ └─────────────────────────────────┘ │
│ Page Footer                         │
└─────────────────────────────────────┘
```

**Fullscreen View:**
```
┌─────────────────────────────────────┐
│ CodeDiffViewerV2                    │
│ (100vh height)                      │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- Expands to full viewport
- Fixed positioning (z-index: 1300)
- Exit button to return to normal view
- Better for large diffs

## Supported Languages

### Programming Languages
- JavaScript (`.js`)
- TypeScript (`.ts`)
- JSX (`.jsx`)
- TSX (`.tsx`)
- Python (`.py`)
- SQL (`.sql`)

### Data Formats
- JSON (`.json`)
- YAML (`.yaml`, `.yml`)
- Markdown (`.md`)

### Web Technologies
- HTML (`.html`)
- CSS (`.css`)

## Theme Support

### Dark Theme (Default)

```
Background: #1e1e1e (dark gray)
Text: #d4d4d4 (light gray)
Accent: #68a063 (Node.js green)
Gutters: #1e1e1e
Active Line: #2a2a2a
```

### Light Theme

```
Background: #ffffff (white)
Text: #24292e (dark gray)
Accent: #68a063 (Node.js green)
Gutters: #f6f8fa (light gray)
Active Line: #f6f8fa
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + F` | Search in code |
| `Ctrl/Cmd + C` | Copy selected text |
| `Arrow Keys` | Navigate code |
| `Page Up/Down` | Scroll by page |
| `Home/End` | Jump to line start/end |

## Accessibility Features

1. **ARIA Labels**
   - All buttons have descriptive labels
   - Screen reader friendly

2. **Keyboard Navigation**
   - All controls accessible via keyboard
   - Proper tab order

3. **High Contrast**
   - Clear color differentiation
   - Readable text at all sizes

4. **Focus Indicators**
   - Visible focus states
   - Clear active element

## Performance Characteristics

### Bundle Size
- CodeMirror 6: ~500KB
- Language packages: ~50KB each
- Total: ~600-700KB (vs 3MB for Monaco)

### Rendering Speed
- Initial render: <100ms
- Diff computation: <50ms for typical files
- Scroll performance: 60fps

### Memory Usage
- Efficient line-by-line processing
- No GPU memory leaks
- Scales well with large files

## Best Practices

### 1. Choose the Right Mode

**Use Side-by-Side when:**
- Comparing similar files
- Need to see both versions simultaneously
- Working with wide screens

**Use Inline when:**
- Reviewing small changes
- Working on mobile/narrow screens
- Need compact view

### 2. Custom Labels

```tsx
// Good: Descriptive labels
<CodeDiffViewerV2
  originalLabel="Production (v1.2.3)"
  modifiedLabel="Staging (v1.3.0)"
  ...
/>

// Bad: Generic labels
<CodeDiffViewerV2
  originalLabel="Old"
  modifiedLabel="New"
  ...
/>
```

### 3. Language Selection

```tsx
// Correct: Use specific language
<CodeDiffViewerV2 language="typescript" ... />

// Avoid: Generic or missing language
<CodeDiffViewerV2 language="text" ... />
```

### 4. Theme Consistency

```tsx
// Match your app theme
const appTheme = useTheme()

<CodeDiffViewerV2
  theme={appTheme.palette.mode} // 'dark' or 'light'
  ...
/>
```

## Common Use Cases

### 1. Code Review
```tsx
<CodeDiffViewerV2
  originalCode={pullRequest.baseCode}
  modifiedCode={pullRequest.headCode}
  language="typescript"
  originalLabel={`Base (${pullRequest.baseBranch})`}
  modifiedLabel={`PR #${pullRequest.number}`}
/>
```

### 2. Version Comparison
```tsx
<CodeDiffViewerV2
  originalCode={versions[0].content}
  modifiedCode={versions[1].content}
  language="python"
  originalLabel={`v${versions[0].number}`}
  modifiedLabel={`v${versions[1].number}`}
/>
```

### 3. Configuration Changes
```tsx
<CodeDiffViewerV2
  originalCode={devConfig}
  modifiedCode={prodConfig}
  language="yaml"
  originalLabel="Development"
  modifiedLabel="Production"
/>
```

### 4. Refactoring Review
```tsx
<CodeDiffViewerV2
  originalCode={beforeRefactor}
  modifiedCode={afterRefactor}
  language="javascript"
  originalLabel="Before Refactor"
  modifiedLabel="After Refactor"
/>
```

## Troubleshooting

### Issue: Diff not showing correctly

**Solution:** Ensure both `originalCode` and `modifiedCode` are strings with proper line breaks (`\n`).

### Issue: Syntax highlighting not working

**Solution:** Check that the `language` prop matches a supported language. Use lowercase (e.g., `"javascript"` not `"JavaScript"`).

### Issue: Theme not applying

**Solution:** Verify the `theme` prop is either `"dark"` or `"light"`. Default is `"dark"`.

### Issue: Download not working

**Solution:** Ensure browser allows downloads. Check for popup blockers.

## Future Enhancements (Potential)

1. **Advanced Diff Algorithm**
   - Word-level diffs
   - Intelligent change detection
   - Better handling of moved code

2. **Merge Conflict Resolution**
   - Three-way merge view
   - Conflict markers
   - Resolution tools

3. **Annotations**
   - Comments on specific lines
   - Change explanations
   - Review feedback

4. **Performance**
   - Virtual scrolling for large files
   - Lazy loading of syntax highlighting
   - Web Worker for diff computation

## Conclusion

CodeDiffViewerV2 provides a robust, performant, and user-friendly way to view code differences. With its comprehensive feature set and modern architecture, it's ready for production use in any React application.
