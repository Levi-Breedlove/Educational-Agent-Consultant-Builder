import { useEffect, useCallback } from 'react'
import { KEYBOARD_KEYS, isActivationKey } from '../utils/accessibility'

interface KeyboardNavigationOptions {
  onEnter?: () => void
  onEscape?: () => void
  onArrowUp?: () => void
  onArrowDown?: () => void
  onArrowLeft?: () => void
  onArrowRight?: () => void
  onHome?: () => void
  onEnd?: () => void
  onSpace?: () => void
}

/**
 * Hook for handling keyboard navigation
 */
export const useKeyboardNavigation = (options: KeyboardNavigationOptions) => {
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      const { key } = event

      switch (key) {
        case KEYBOARD_KEYS.ENTER:
          if (options.onEnter) {
            event.preventDefault()
            options.onEnter()
          }
          break
        case KEYBOARD_KEYS.SPACE:
          if (options.onSpace) {
            event.preventDefault()
            options.onSpace()
          }
          break
        case KEYBOARD_KEYS.ESCAPE:
          if (options.onEscape) {
            event.preventDefault()
            options.onEscape()
          }
          break
        case KEYBOARD_KEYS.ARROW_UP:
          if (options.onArrowUp) {
            event.preventDefault()
            options.onArrowUp()
          }
          break
        case KEYBOARD_KEYS.ARROW_DOWN:
          if (options.onArrowDown) {
            event.preventDefault()
            options.onArrowDown()
          }
          break
        case KEYBOARD_KEYS.ARROW_LEFT:
          if (options.onArrowLeft) {
            event.preventDefault()
            options.onArrowLeft()
          }
          break
        case KEYBOARD_KEYS.ARROW_RIGHT:
          if (options.onArrowRight) {
            event.preventDefault()
            options.onArrowRight()
          }
          break
        case KEYBOARD_KEYS.HOME:
          if (options.onHome) {
            event.preventDefault()
            options.onHome()
          }
          break
        case KEYBOARD_KEYS.END:
          if (options.onEnd) {
            event.preventDefault()
            options.onEnd()
          }
          break
      }
    },
    [options]
  )

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [handleKeyDown])
}

/**
 * Hook for making an element keyboard-activatable (Enter/Space)
 */
export const useKeyboardActivation = (onActivate: () => void) => {
  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent) => {
      if (isActivationKey(event.key)) {
        event.preventDefault()
        onActivate()
      }
    },
    [onActivate]
  )

  return {
    onKeyDown: handleKeyDown,
    role: 'button',
    tabIndex: 0,
  }
}

export default {
  useKeyboardNavigation,
  useKeyboardActivation,
}
