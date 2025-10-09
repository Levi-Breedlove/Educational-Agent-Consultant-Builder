# Developer Guide - Agent Builder Frontend

Quick reference for developers working on the Agent Builder Platform frontend.

## Quick Start

```bash
cd agent-builder-platform/frontend
npm install
npm run dev
```

Frontend: http://localhost:3000  
Backend: http://localhost:8000 (must be running)

## Project Structure

```
src/
├── api/          # API client and endpoints
├── components/   # React components
├── pages/        # Page components
├── store/        # Redux state management
├── hooks/        # Custom React hooks
├── theme/        # Material-UI theming
└── utils/        # Utility functions
```

## Key Technologies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Redux Toolkit** - State management
- **React Query** - Server state
- **Material-UI** - Components
- **React Router** - Routing

## State Management

### Redux Slices

```typescript
// Session state
const { sessionId, agentId, isConnected } = useSelector(state => state.session)

// Workflow state
const { currentPhase, progress, elapsedTime } = useSelector(state => state.workflow)

// UI state
const { theme, sidebarOpen, isMobile } = useSelector(state => state.ui)
```

### Dispatch Actions

```typescript
import { setSession, setConnected } from './store/slices/sessionSlice'
import { setPhase, setProgress } from './store/slices/workflowSlice'
import { toggleTheme, setIsMobile } from './store/slices/uiSlice'

dispatch(setSession({ sessionId, agentId }))
dispatch(setPhase('architecture'))
dispatch(toggleTheme())
```

## API Integration

### Using React Query

```typescript
import { useQuery, useMutation } from '@tanstack/react-query'
import { sessionsApi, agentsApi } from './api'

// Query
const { data, isLoading, error } = useQuery({
  queryKey: ['session', sessionId],
  queryFn: () => sessionsApi.get(sessionId),
})

// Mutation
const mutation = useMutation({
  mutationFn: sessionsApi.create,
  onSuccess: (data) => {
    // Handle success
  },
})
```

### WebSocket Connection

```typescript
import useWebSocket from './hooks/useWebSocket'

const { sendMessage, lastMessage, isConnected } = useWebSocket(
  `ws://localhost:8000/ws/agents/${agentId}`
)
```

## Custom Hooks

### Responsive Design

```typescript
import useResponsive from './hooks/useResponsive'

const { isMobile, isTablet, isDesktop } = useResponsive()
```

### Theme Detection

```typescript
import useSystemTheme from './hooks/useSystemTheme'

useSystemTheme() // Auto-updates theme based on system preference
```

### Keyboard Navigation

```typescript
import { useKeyboardNavigation } from './hooks/useKeyboardNavigation'

useKeyboardNavigation({
  onEnter: handleSubmit,
  onEscape: handleClose,
  onArrowDown: handleNext,
})
```

### Focus Management

```typescript
import { useFocusManagement, useFocusTrap } from './hooks/useFocusManagement'

// Save/restore focus for modals
const previousFocusRef = useFocusManagement(isOpen)

// Trap focus in container
const containerRef = useFocusTrap(isActive)
```

## Components

### Chat Interface

```typescript
import ChatInterface from './components/ChatInterface'

<ChatInterface />
```

### Progress Tracker

```typescript
import ProgressTracker from './components/ProgressTracker'

<ProgressTracker />
```

### Loading Skeletons

```typescript
import { ChatInterfaceSkeleton, ProgressTrackerSkeleton } from './components/LoadingSkeletons'

{isLoading ? <ChatInterfaceSkeleton /> : <ChatInterface />}
```

### Accessible Form

```typescript
import AccessibleTextField from './components/AccessibleForm'

<AccessibleTextField
  label="Email"
  value={email}
  onChange={setEmail}
  error={emailError}
  required
/>
```

## Theming

### Using Theme

```typescript
import { useTheme } from '@mui/material/styles'

const theme = useTheme()
const isMobile = useMediaQuery(theme.breakpoints.down('md'))
```

### Custom Styles

```typescript
<Box
  sx={{
    p: { xs: 2, sm: 3, md: 4 },  // Responsive padding
    fontSize: { xs: '0.9rem', sm: '1rem' },  // Responsive font
    display: { xs: 'none', md: 'block' },  // Hide on mobile
  }}
>
```

### Theme Toggle

```typescript
import { toggleTheme, setSystemTheme } from './store/slices/uiSlice'

dispatch(toggleTheme())  // Toggle between light/dark
dispatch(setSystemTheme())  // Use system preference
```

## Accessibility

### ARIA Labels

```typescript
<IconButton
  aria-label="Open menu"
  aria-expanded={isOpen}
  aria-controls="menu-id"
>
```

### Screen Reader Announcements

```typescript
import { announceToScreenReader } from './utils/accessibility'

announceToScreenReader('Form submitted successfully', 'polite')
```

### Keyboard Activation

```typescript
import { useKeyboardActivation } from './hooks/useKeyboardNavigation'

const props = useKeyboardActivation(handleClick)
<div {...props}>Clickable element</div>
```

## Routing

```typescript
import { useNavigate, useParams, useLocation } from 'react-router-dom'

const navigate = useNavigate()
const { agentId } = useParams()
const location = useLocation()

navigate('/builder')
navigate(`/builder/${agentId}`)
```

## Environment Variables

```env
VITE_API_URL=http://localhost:8000
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

## Common Patterns

### Conditional Rendering

```typescript
{isLoading && <Skeleton />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}
```

### Responsive Layout

```typescript
<Grid container spacing={2}>
  <Grid item xs={12} md={8}>
    <ChatInterface />
  </Grid>
  <Grid item xs={12} md={4}>
    <ProgressTracker />
  </Grid>
</Grid>
```

### Error Handling

```typescript
try {
  const result = await apiCall()
  dispatch(setSuccess(result))
} catch (error) {
  dispatch(setError(error.message))
  announceToScreenReader('An error occurred', 'assertive')
}
```

## Testing

### Run Tests

```bash
npm run lint  # ESLint
```

### Accessibility Testing

```typescript
import { runAccessibilityAudit } from './utils/accessibilityTesting'

// In development
if (process.env.NODE_ENV === 'development') {
  runAccessibilityAudit()
}
```

### Manual Testing Checklist

- [ ] Test on mobile (< 600px)
- [ ] Test on tablet (600-960px)
- [ ] Test on desktop (> 960px)
- [ ] Test keyboard navigation
- [ ] Test with screen reader
- [ ] Test theme toggle
- [ ] Test all interactive elements

## Build & Deploy

### Development

```bash
npm run dev  # Start dev server
```

### Production Build

```bash
npm run build  # Build for production
npm run preview  # Preview production build
```

### Build Output

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── ...
```

## Troubleshooting

### Port Already in Use

Change port in `vite.config.ts`:
```typescript
server: {
  port: 3001,
}
```

### Backend Connection Issues

1. Verify backend is running at http://localhost:8000
2. Check `VITE_API_URL` in `.env`
3. Check proxy configuration in `vite.config.ts`

### Theme Not Persisting

Check localStorage:
```javascript
localStorage.getItem('theme')
localStorage.getItem('themeSource')
```

### WebSocket Connection Fails

1. Verify WebSocket endpoint: `ws://localhost:8000/ws/agents/:id`
2. Check backend WebSocket implementation
3. Check browser console for errors

## Best Practices

### Component Structure

```typescript
// 1. Imports
import { useState } from 'react'
import { Box, Button } from '@mui/material'

// 2. Types/Interfaces
interface MyComponentProps {
  title: string
  onSubmit: () => void
}

// 3. Component
export default function MyComponent({ title, onSubmit }: MyComponentProps) {
  // 4. Hooks
  const [value, setValue] = useState('')
  
  // 5. Handlers
  const handleClick = () => {
    onSubmit()
  }
  
  // 6. Render
  return (
    <Box>
      <Button onClick={handleClick}>{title}</Button>
    </Box>
  )
}
```

### State Management

- Use Redux for global state (session, workflow, UI)
- Use React Query for server state (API calls)
- Use local state (useState) for component-specific state

### Accessibility

- Always add `aria-label` to icon buttons
- Use semantic HTML (`<button>`, `<nav>`, `<main>`)
- Ensure keyboard navigation works
- Test with screen readers
- Maintain color contrast (4.5:1 minimum)

### Performance

- Use React.memo for expensive components
- Lazy load routes with React.lazy
- Optimize images and assets
- Use loading skeletons
- Debounce expensive operations

## Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Material-UI Documentation](https://mui.com/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Support

- Check `README.md` for detailed documentation
- Check `ACCESSIBILITY-GUIDE.md` for accessibility features
- Check `TASK-*.md` files for implementation details
- Create an issue in the repository for bugs

---

**Happy Coding!** 🚀
