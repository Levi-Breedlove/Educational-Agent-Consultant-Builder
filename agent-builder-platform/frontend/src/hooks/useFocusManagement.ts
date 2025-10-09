import { useEffect, useRef } from 'react'
import { saveFocus, restoreFocus } from '../utils/accessibility'

/**
 * Hook to manage focus when component mounts/unmounts
 * Useful for modals and dialogs
 */
export const useFocusManagement = (isOpen: boolean) => {
  const previousFocusRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Save current focus
      previousFocusRef.current = saveFocus()
    } else {
      // Restore previous focus
      restoreFocus(previousFocusRef.current)
    }
  }, [isOpen])

  return previousFocusRef
}

/**
 * Hook to auto-focus an element when component mounts
 */
export const useAutoFocus = <T extends HTMLElement>() => {
  const elementRef = useRef<T>(null)

  useEffect(() => {
    if (elementRef.current) {
      elementRef.current.focus()
    }
  }, [])

  return elementRef
}

/**
 * Hook to trap focus within a container
 */
export const useFocusTrap = <T extends HTMLElement>(isActive: boolean) => {
  const containerRef = useRef<T>(null)

  useEffect(() => {
    if (!isActive || !containerRef.current) return

    const container = containerRef.current
    const focusableElements = container.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )

    const firstElement = focusableElements[0]
    const lastElement = focusableElements[focusableElements.length - 1]

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement?.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement?.focus()
          e.preventDefault()
        }
      }
    }

    container.addEventListener('keydown', handleTabKey)

    // Focus first element
    firstElement?.focus()

    return () => {
      container.removeEventListener('keydown', handleTabKey)
    }
  }, [isActive])

  return containerRef
}

export default {
  useFocusManagement,
  useAutoFocus,
  useFocusTrap,
}
