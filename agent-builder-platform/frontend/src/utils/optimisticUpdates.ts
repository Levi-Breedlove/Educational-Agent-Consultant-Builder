/**
 * Optimistic update utilities for better perceived performance
 * 
 * Requirements: 12.2
 */

/**
 * Optimistic update state
 */
export interface OptimisticUpdate<T> {
  id: string
  data: T
  isPending: boolean
  error?: Error
}

/**
 * Create an optimistic update manager
 * Manages temporary optimistic updates while waiting for server confirmation
 */
export class OptimisticUpdateManager<T> {
  private updates: Map<string, OptimisticUpdate<T>> = new Map()
  private listeners: Set<() => void> = new Set()

  /**
   * Add an optimistic update
   */
  add(id: string, data: T): void {
    this.updates.set(id, {
      id,
      data,
      isPending: true,
    })
    this.notify()
  }

  /**
   * Confirm an optimistic update (server responded successfully)
   */
  confirm(id: string): void {
    this.updates.delete(id)
    this.notify()
  }

  /**
   * Reject an optimistic update (server responded with error)
   */
  reject(id: string, error: Error): void {
    const update = this.updates.get(id)
    if (update) {
      this.updates.set(id, {
        ...update,
        isPending: false,
        error,
      })
      this.notify()
    }
  }

  /**
   * Get all pending updates
   */
  getPending(): OptimisticUpdate<T>[] {
    return Array.from(this.updates.values()).filter(u => u.isPending)
  }

  /**
   * Get all failed updates
   */
  getFailed(): OptimisticUpdate<T>[] {
    return Array.from(this.updates.values()).filter(u => !u.isPending && u.error)
  }

  /**
   * Clear all updates
   */
  clear(): void {
    this.updates.clear()
    this.notify()
  }

  /**
   * Subscribe to changes
   */
  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  /**
   * Notify all listeners
   */
  private notify(): void {
    this.listeners.forEach(listener => listener())
  }
}

/**
 * Merge optimistic updates with server data
 */
export function mergeOptimisticData<T extends { id: string }>(
  serverData: T[],
  optimisticUpdates: OptimisticUpdate<T>[]
): T[] {
  const merged = [...serverData]
  
  // Add pending optimistic updates
  for (const update of optimisticUpdates) {
    if (update.isPending) {
      // Check if item already exists in server data
      const existingIndex = merged.findIndex(item => item.id === update.data.id)
      if (existingIndex >= 0) {
        // Update existing item
        merged[existingIndex] = update.data
      } else {
        // Add new item
        merged.push(update.data)
      }
    }
  }
  
  return merged
}

/**
 * Create a debounced function for optimistic updates
 * Useful for input fields that trigger server updates
 */
export function createOptimisticDebounce<T extends any[]>(
  fn: (...args: T) => Promise<void>,
  delay: number = 500
): (...args: T) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let pendingArgs: T | null = null

  return (...args: T) => {
    pendingArgs = args

    if (timeoutId) {
      clearTimeout(timeoutId)
    }

    timeoutId = setTimeout(async () => {
      if (pendingArgs) {
        try {
          await fn(...pendingArgs)
        } catch (error) {
          console.error('Optimistic update failed:', error)
        }
        pendingArgs = null
      }
    }, delay)
  }
}

export default OptimisticUpdateManager
