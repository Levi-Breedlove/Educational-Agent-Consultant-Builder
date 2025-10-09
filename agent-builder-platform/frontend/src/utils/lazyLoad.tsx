import React, { Suspense, ComponentType, LazyExoticComponent } from 'react'
import { Box, CircularProgress } from '@mui/material'

/**
 * Loading fallback component
 */
const LoadingFallback: React.FC<{ minHeight?: number }> = ({ minHeight = 200 }) => (
  <Box
    sx={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: `${minHeight}px`,
      width: '100%',
    }}
    role="status"
    aria-label="Loading content"
  >
    <CircularProgress />
  </Box>
)

/**
 * Lazy load a component with automatic Suspense wrapper
 * 
 * Usage:
 * const MyComponent = lazyLoad(() => import('./MyComponent'))
 */
export function lazyLoad<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>,
  fallback?: React.ReactNode
): React.FC<React.ComponentProps<T>> {
  const LazyComponent = React.lazy(importFunc)

  return (props: React.ComponentProps<T>) => (
    <Suspense fallback={fallback || <LoadingFallback />}>
      <LazyComponent {...props} />
    </Suspense>
  )
}

/**
 * Preload a lazy component
 * Useful for prefetching components before they're needed
 * 
 * Usage:
 * const MyComponent = React.lazy(() => import('./MyComponent'))
 * preloadComponent(MyComponent)
 */
export function preloadComponent<T extends ComponentType<any>>(
  component: LazyExoticComponent<T>
): void {
  // Access the _payload to trigger the import
  const payload = (component as any)._payload
  if (payload && typeof payload._result === 'undefined') {
    payload._result
  }
}

/**
 * Create a lazy loaded route component
 * Optimized for React Router
 */
export function lazyRoute<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>
): LazyExoticComponent<T> {
  return React.lazy(importFunc)
}

export default lazyLoad
