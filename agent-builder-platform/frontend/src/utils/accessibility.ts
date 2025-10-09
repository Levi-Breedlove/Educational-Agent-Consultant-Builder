/**
 * Accessibility utilities for WCAG 2.1 AA compliance
 */

// Announce to screen readers
export const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
  const announcement = document.createElement('div')
  announcement.setAttribute('role', 'status')
  announcement.setAttribute('aria-live', priority)
  announcement.setAttribute('aria-atomic', 'true')
  announcement.className = 'sr-only'
  announcement.textContent = message
  
  document.body.appendChild(announcement)
  
  // Remove after announcement
  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

// Trap focus within a container (for modals/dialogs)
export const trapFocus = (element: HTMLElement) => {
  const focusableElements = element.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  
  const firstFocusable = focusableElements[0]
  const lastFocusable = focusableElements[focusableElements.length - 1]
  
  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return
    
    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        lastFocusable.focus()
        e.preventDefault()
      }
    } else {
      if (document.activeElement === lastFocusable) {
        firstFocusable.focus()
        e.preventDefault()
      }
    }
  }
  
  element.addEventListener('keydown', handleTabKey)
  
  return () => {
    element.removeEventListener('keydown', handleTabKey)
  }
}

// Check if element is visible to screen readers
export const isVisibleToScreenReader = (element: HTMLElement): boolean => {
  return (
    element.getAttribute('aria-hidden') !== 'true' &&
    element.style.display !== 'none' &&
    element.style.visibility !== 'hidden'
  )
}

// Generate unique ID for ARIA relationships
let idCounter = 0
export const generateAriaId = (prefix: string = 'aria'): string => {
  idCounter++
  return `${prefix}-${idCounter}-${Date.now()}`
}

// Keyboard navigation helpers
export const KEYBOARD_KEYS = {
  ENTER: 'Enter',
  SPACE: ' ',
  ESCAPE: 'Escape',
  TAB: 'Tab',
  ARROW_UP: 'ArrowUp',
  ARROW_DOWN: 'ArrowDown',
  ARROW_LEFT: 'ArrowLeft',
  ARROW_RIGHT: 'ArrowRight',
  HOME: 'Home',
  END: 'End',
} as const

export const isActivationKey = (key: string): boolean => {
  return key === KEYBOARD_KEYS.ENTER || key === KEYBOARD_KEYS.SPACE
}

// Focus management
export const saveFocus = (): HTMLElement | null => {
  return document.activeElement as HTMLElement
}

export const restoreFocus = (element: HTMLElement | null) => {
  if (element && element.focus) {
    element.focus()
  }
}

// Skip link helper
export const scrollToMain = () => {
  const main = document.querySelector('main')
  if (main) {
    main.focus()
    main.scrollIntoView({ behavior: 'smooth' })
  }
}
