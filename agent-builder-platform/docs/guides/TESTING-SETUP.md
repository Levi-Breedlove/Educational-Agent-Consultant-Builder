# Testing Setup for Task 14 Components

## Required Dependencies

To run the tests for the confidence dashboard and performance components, install these dependencies:

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

## Vitest Configuration

Create `vitest.config.ts`:

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

## Test Setup File

Create `src/test/setup.ts`:

```typescript
import '@testing-library/jest-dom'
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Cleanup after each test
afterEach(() => {
  cleanup()
})
```

## Update package.json Scripts

Add test scripts to `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests once
npm run test:run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Existing Test Files

- `src/components/__tests__/ConfidenceDashboard.test.tsx` - Tests for confidence dashboard component

## Test Coverage Goals

- ✅ Confidence score rendering
- ✅ Baseline threshold alerts
- ✅ Factor breakdown display
- ✅ Confidence boosters/uncertainties
- ✅ Recommended actions
- ✅ Expandable/collapsible behavior
- ✅ Accessibility features

## Additional Tests to Add

### WebSocket Hooks
```typescript
// src/hooks/__tests__/useWebSocket.test.ts
// src/hooks/__tests__/useConfidenceUpdates.test.ts
// src/hooks/__tests__/useStreamingResponse.test.ts
```

### Performance Utilities
```typescript
// src/utils/__tests__/lazyLoad.test.tsx
// src/utils/__tests__/optimisticUpdates.test.ts
// src/hooks/__tests__/useVirtualScroll.test.ts
```

### Image Optimization
```typescript
// src/components/__tests__/OptimizedImage.test.tsx
```

## Mock Setup for WebSocket

Create `src/test/mocks/websocket.ts`:

```typescript
export class MockWebSocket {
  static CONNECTING = 0
  static OPEN = 1
  static CLOSING = 2
  static CLOSED = 3

  readyState = MockWebSocket.CONNECTING
  onopen: ((event: Event) => void) | null = null
  onclose: ((event: CloseEvent) => void) | null = null
  onmessage: ((event: MessageEvent) => void) | null = null
  onerror: ((event: Event) => void) | null = null

  constructor(public url: string) {
    setTimeout(() => {
      this.readyState = MockWebSocket.OPEN
      this.onopen?.(new Event('open'))
    }, 0)
  }

  send(data: string) {
    // Mock send
  }

  close() {
    this.readyState = MockWebSocket.CLOSED
    this.onclose?.(new CloseEvent('close'))
  }
}

global.WebSocket = MockWebSocket as any
```

## Notes

- The test file `ConfidenceDashboard.test.tsx` is ready but requires dependencies
- Install testing libraries when ready to run tests
- All components are designed to be testable with proper props and behavior
- WebSocket hooks will need mocking for tests
