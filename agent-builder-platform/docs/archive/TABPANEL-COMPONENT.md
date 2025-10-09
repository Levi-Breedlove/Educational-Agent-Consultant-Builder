# TabPanel Component Documentation

## Overview

The `TabPanel` component is a reusable, accessible tab panel implementation that manages visibility and ARIA attributes for tabbed interfaces. It follows WAI-ARIA best practices for tab panels and provides a clean API for building tabbed UIs.

## Features

- ✅ **Accessibility**: Full ARIA support with proper roles and attributes
- ✅ **Performance**: Optional keep-mounted mode for performance optimization
- ✅ **Flexibility**: Customizable ID prefixes for multiple tab groups
- ✅ **Type Safety**: Full TypeScript support with proper types
- ✅ **Testing**: 100% test coverage (7/7 tests passing)

## Installation

The component is already exported from the components index:

```typescript
import { TabPanel, a11yProps } from '../components'
```

## Basic Usage

### Simple Tab Panel

```tsx
import { useState } from 'react'
import { Tabs, Tab, Box } from '@mui/material'
import { TabPanel, a11yProps } from '../components'

function MyTabbedInterface() {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <Box>
      <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
        <Tab label="Chat" {...a11yProps(0)} />
        <Tab label="Architecture" {...a11yProps(1)} />
        <Tab label="Code" {...a11yProps(2)} />
      </Tabs>

      <TabPanel value={activeTab} index={0}>
        <ChatInterface />
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <ArchitectureVisualizer />
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <CodeWorkspace />
      </TabPanel>
    </Box>
  )
}
```

### With Keep-Mounted Mode

Use `keepMounted` to keep inactive tabs in the DOM (useful for preserving state):

```tsx
<TabPanel value={activeTab} index={0} keepMounted>
  <ExpensiveComponent />
</TabPanel>
```

### Custom ID Prefix

Use custom ID prefixes when you have multiple tab groups on the same page:

```tsx
<Tabs value={activeTab} onChange={handleChange}>
  <Tab label="Tab 1" {...a11yProps(0, 'main')} />
  <Tab label="Tab 2" {...a11yProps(1, 'main')} />
</Tabs>

<TabPanel value={activeTab} index={0} id="main">
  <Content1 />
</TabPanel>

<TabPanel value={activeTab} index={1} id="main">
  <Content2 />
</TabPanel>
```

## API Reference

### TabPanel Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Content to display in the tab panel |
| `index` | `number` | - | The index of this tab panel (required) |
| `value` | `number` | - | The currently active tab index (required) |
| `keepMounted` | `boolean` | `false` | If true, keeps the panel mounted in DOM when hidden |
| `id` | `string` | `'tab'` | ID prefix for ARIA attributes |

### a11yProps Function

Helper function to generate ARIA props for tab buttons.

**Signature:**
```typescript
function a11yProps(index: number, id?: string): {
  id: string
  'aria-controls': string
}
```

**Parameters:**
- `index` (number): The index of the tab
- `id` (string, optional): ID prefix (default: 'tab')

**Returns:**
- Object with `id` and `aria-controls` props

**Example:**
```tsx
<Tab label="My Tab" {...a11yProps(0)} />
// Generates: { id: 'tab-0', 'aria-controls': 'tab-panel-0' }

<Tab label="My Tab" {...a11yProps(0, 'custom')} />
// Generates: { id: 'custom-0', 'aria-controls': 'custom-panel-0' }
```

## Accessibility

The TabPanel component follows WAI-ARIA best practices:

### ARIA Attributes

- `role="tabpanel"`: Identifies the element as a tab panel
- `id`: Unique identifier for the panel
- `aria-labelledby`: References the controlling tab button
- `hidden`: Indicates visibility state

### Keyboard Navigation

The TabPanel component works seamlessly with Material-UI's Tabs component, which provides:

- **Arrow Keys**: Navigate between tabs
- **Home/End**: Jump to first/last tab
- **Tab**: Move focus to tab panel content
- **Enter/Space**: Activate focused tab

### Screen Reader Support

- Announces tab panel role and label
- Indicates active/inactive state
- Properly associates panels with their controlling tabs

## Performance Considerations

### Default Behavior (Unmount Inactive)

By default, inactive tab panels are unmounted from the DOM:

```tsx
<TabPanel value={activeTab} index={0}>
  <Component /> {/* Unmounted when not active */}
</TabPanel>
```

**Pros:**
- Lower memory usage
- Faster initial render
- Cleaner DOM

**Cons:**
- State is lost when switching tabs
- Re-renders when returning to tab

### Keep-Mounted Mode

Use `keepMounted` to keep inactive panels in the DOM:

```tsx
<TabPanel value={activeTab} index={0} keepMounted>
  <Component /> {/* Always mounted, just hidden */}
</TabPanel>
```

**Pros:**
- Preserves component state
- No re-render when switching back
- Useful for forms, media players, etc.

**Cons:**
- Higher memory usage
- Slower initial render
- More DOM nodes

### Recommendations

- Use default mode for simple content (text, images)
- Use `keepMounted` for:
  - Forms with user input
  - Media players (video, audio)
  - Complex state that's expensive to recreate
  - Real-time data streams

## Integration with Redux

For managing tab state across the application:

```typescript
// In uiSlice.ts
interface UIState {
  activeTab: 'chat' | 'architecture' | 'code' | 'confidence'
  tabHistory: string[]
}

// In component
import { useSelector, useDispatch } from 'react-redux'
import { setActiveTab } from '../store/slices/uiSlice'

function MyComponent() {
  const activeTab = useSelector((state) => state.ui.activeTab)
  const dispatch = useDispatch()

  const tabIndexMap = {
    chat: 0,
    architecture: 1,
    code: 2,
    confidence: 3,
  }

  return (
    <TabPanel value={tabIndexMap[activeTab]} index={0}>
      <ChatInterface />
    </TabPanel>
  )
}
```

## Testing

The component has 100% test coverage with 7 passing tests:

```bash
npm test -- TabPanel.test.tsx --run
```

### Test Coverage

- ✅ Renders children when active
- ✅ Hides content when not active
- ✅ Keeps content mounted when keepMounted is true
- ✅ Has correct ARIA attributes
- ✅ Uses default id when not provided
- ✅ a11yProps generates correct props with default id
- ✅ a11yProps generates correct props with custom id

## Examples

### Full AgentBuilderPage Integration

```tsx
import { useState } from 'react'
import { Box, Tabs, Tab } from '@mui/material'
import { Chat, Architecture, Code, CheckCircle } from '@mui/icons-material'
import { TabPanel, a11yProps } from '../components'

export default function AgentBuilderPage() {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Tab Navigation */}
      <Tabs
        value={activeTab}
        onChange={(e, newValue) => setActiveTab(newValue)}
        aria-label="agent builder tabs"
      >
        <Tab icon={<Chat />} label="Chat" {...a11yProps(0, 'builder')} />
        <Tab icon={<Architecture />} label="Architecture" {...a11yProps(1, 'builder')} />
        <Tab icon={<Code />} label="Code" {...a11yProps(2, 'builder')} />
        <Tab icon={<CheckCircle />} label="Confidence" {...a11yProps(3, 'builder')} />
      </Tabs>

      {/* Tab Content */}
      <Box sx={{ flex: 1, overflow: 'hidden' }}>
        <TabPanel value={activeTab} index={0} id="builder">
          <ChatInterface />
        </TabPanel>

        <TabPanel value={activeTab} index={1} id="builder">
          <ArchitectureVisualizer />
        </TabPanel>

        <TabPanel value={activeTab} index={2} id="builder" keepMounted>
          <CodeWorkspace />
        </TabPanel>

        <TabPanel value={activeTab} index={3} id="builder">
          <ConfidenceHistory />
        </TabPanel>
      </Box>
    </Box>
  )
}
```

### Responsive Mobile Tabs

```tsx
import { useMediaQuery, useTheme } from '@mui/material'

function ResponsiveTabs() {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const [activeTab, setActiveTab] = useState(0)

  return (
    <Box>
      <Tabs
        value={activeTab}
        onChange={(e, newValue) => setActiveTab(newValue)}
        variant={isMobile ? 'scrollable' : 'standard'}
        scrollButtons={isMobile ? 'auto' : false}
      >
        <Tab label="Tab 1" {...a11yProps(0)} />
        <Tab label="Tab 2" {...a11yProps(1)} />
        <Tab label="Tab 3" {...a11yProps(2)} />
      </Tabs>

      <TabPanel value={activeTab} index={0}>
        <Content1 />
      </TabPanel>
      <TabPanel value={activeTab} index={1}>
        <Content2 />
      </TabPanel>
      <TabPanel value={activeTab} index={2}>
        <Content3 />
      </TabPanel>
    </Box>
  )
}
```

## Related Components

- **Material-UI Tabs**: Tab navigation component
- **Material-UI Tab**: Individual tab button
- **Layout**: Main application layout
- **SkipLink**: Accessibility navigation

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## License

Part of the Agent Builder Platform project.
