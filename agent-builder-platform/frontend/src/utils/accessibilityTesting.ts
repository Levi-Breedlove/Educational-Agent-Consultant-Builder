/**
 * Accessibility testing utilities
 * These help identify accessibility issues during development
 */

export interface AccessibilityIssue {
  type: 'error' | 'warning'
  element: HTMLElement
  message: string
  wcagCriterion?: string
}

/**
 * Check for missing alt text on images
 */
export const checkImageAltText = (): AccessibilityIssue[] => {
  const issues: AccessibilityIssue[] = []
  const images = document.querySelectorAll('img')

  images.forEach((img) => {
    if (!img.hasAttribute('alt')) {
      issues.push({
        type: 'error',
        element: img,
        message: 'Image missing alt attribute',
        wcagCriterion: 'WCAG 1.1.1 (Level A)',
      })
    }
  })

  return issues
}

/**
 * Check for proper heading hierarchy
 */
export const checkHeadingHierarchy = (): AccessibilityIssue[] => {
  const issues: AccessibilityIssue[] = []
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6')
  let previousLevel = 0

  headings.forEach((heading) => {
    const level = parseInt(heading.tagName.substring(1))

    if (previousLevel > 0 && level > previousLevel + 1) {
      issues.push({
        type: 'warning',
        element: heading as HTMLElement,
        message: `Heading level skipped from h${previousLevel} to h${level}`,
        wcagCriterion: 'WCAG 1.3.1 (Level A)',
      })
    }

    previousLevel = level
  })

  return issues
}

/**
 * Check for proper form labels
 */
export const checkFormLabels = (): AccessibilityIssue[] => {
  const issues: AccessibilityIssue[] = []
  const inputs = document.querySelectorAll('input, select, textarea')

  inputs.forEach((input) => {
    const hasLabel =
      input.hasAttribute('aria-label') ||
      input.hasAttribute('aria-labelledby') ||
      document.querySelector(`label[for="${input.id}"]`)

    if (!hasLabel) {
      issues.push({
        type: 'error',
        element: input as HTMLElement,
        message: 'Form control missing label',
        wcagCriterion: 'WCAG 3.3.2 (Level A)',
      })
    }
  })

  return issues
}

/**
 * Check for sufficient color contrast
 * Note: This is a simplified check. Use tools like axe-core for comprehensive testing
 */
export const checkColorContrast = (): AccessibilityIssue[] => {
  const issues: AccessibilityIssue[] = []
  // This would require complex color contrast calculation
  // Recommend using browser extensions or axe-core for accurate testing
  return issues
}

/**
 * Check for keyboard accessibility
 */
export const checkKeyboardAccessibility = (): AccessibilityIssue[] => {
  const issues: AccessibilityIssue[] = []
  const interactiveElements = document.querySelectorAll(
    'a, button, input, select, textarea, [role="button"], [role="link"]'
  )

  interactiveElements.forEach((element) => {
    const tabIndex = element.getAttribute('tabindex')
    if (tabIndex && parseInt(tabIndex) < 0 && element.tagName !== 'INPUT') {
      issues.push({
        type: 'warning',
        element: element as HTMLElement,
        message: 'Interactive element not keyboard accessible (tabindex < 0)',
        wcagCriterion: 'WCAG 2.1.1 (Level A)',
      })
    }
  })

  return issues
}

/**
 * Run all accessibility checks
 */
export const runAccessibilityAudit = (): AccessibilityIssue[] => {
  return [
    ...checkImageAltText(),
    ...checkHeadingHierarchy(),
    ...checkFormLabels(),
    ...checkColorContrast(),
    ...checkKeyboardAccessibility(),
  ]
}

/**
 * Log accessibility issues to console (development only)
 */
export const logAccessibilityIssues = () => {
  if (import.meta.env.MODE !== 'development') return

  const issues = runAccessibilityAudit()

  if (issues.length === 0) {
    console.log('✅ No accessibility issues found')
    return
  }

  console.group('⚠️ Accessibility Issues Found')
  issues.forEach((issue) => {
    const logFn = issue.type === 'error' ? console.error : console.warn
    logFn(`${issue.message} (${issue.wcagCriterion})`, issue.element)
  })
  console.groupEnd()
}

export default {
  checkImageAltText,
  checkHeadingHierarchy,
  checkFormLabels,
  checkColorContrast,
  checkKeyboardAccessibility,
  runAccessibilityAudit,
  logAccessibilityIssues,
}
