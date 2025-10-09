import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * Virtual scroll configuration
 */
export interface VirtualScrollConfig {
  itemHeight: number // Height of each item in pixels
  containerHeight: number // Height of the scrollable container
  overscan?: number // Number of items to render outside viewport (default: 3)
}

/**
 * Virtual scroll result
 */
export interface VirtualScrollResult {
  virtualItems: Array<{
    index: number
    start: number
    size: number
  }>
  totalHeight: number
  scrollToIndex: (index: number) => void
  containerRef: React.RefObject<HTMLDivElement>
}

/**
 * Hook for virtual scrolling large lists
 * Renders only visible items for better performance
 * 
 * Requirements: 12.2
 * 
 * Usage:
 * const { virtualItems, totalHeight, containerRef } = useVirtualScroll({
 *   itemCount: 10000,
 *   itemHeight: 50,
 *   containerHeight: 600,
 * })
 */
export function useVirtualScroll(
  itemCount: number,
  config: VirtualScrollConfig
): VirtualScrollResult {
  const { itemHeight, containerHeight, overscan = 3 } = config
  const [scrollTop, setScrollTop] = useState(0)
  const containerRef = useRef<HTMLDivElement>(null)

  // Calculate visible range
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan)
  const endIndex = Math.min(
    itemCount - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  )

  // Generate virtual items
  const virtualItems = []
  for (let i = startIndex; i <= endIndex; i++) {
    virtualItems.push({
      index: i,
      start: i * itemHeight,
      size: itemHeight,
    })
  }

  // Total height of all items
  const totalHeight = itemCount * itemHeight

  // Handle scroll events
  const handleScroll = useCallback((e: Event) => {
    const target = e.target as HTMLDivElement
    setScrollTop(target.scrollTop)
  }, [])

  // Scroll to specific index
  const scrollToIndex = useCallback((index: number) => {
    if (containerRef.current) {
      const scrollTop = index * itemHeight
      containerRef.current.scrollTop = scrollTop
      setScrollTop(scrollTop)
    }
  }, [itemHeight])

  // Attach scroll listener
  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    container.addEventListener('scroll', handleScroll, { passive: true })
    return () => container.removeEventListener('scroll', handleScroll)
  }, [handleScroll])

  return {
    virtualItems,
    totalHeight,
    scrollToIndex,
    containerRef,
  }
}

export default useVirtualScroll
