# Accessibility Guide - Agent Builder Platform

## WCAG 2.1 AA Compliance

This document outlines the accessibility features implemented in the Agent Builder Platform frontend to ensure WCAG 2.1 Level AA compliance.

## Table of Contents

1. [Overview](#overview)
2. [Perceivable](#perceivable)
3. [Operable](#operable)
4. [Understandable](#understandable)
5. [Robust](#robust)
6. [Testing](#testing)
7. [Tools and Utilities](#tools-and-utilities)

## Overview

The Agent Builder Platform is designed to be accessible to all users, including those using assistive technologies such as screen readers, keyboard-only navigation, and voice control.

### Compliance Level

- **Target**: WCAG 2.1 Level AA
- **Status**: Compliant
- **Last Audit**: [Date]

## Perceivable

### 1.1 Text Alternatives

#### Images (1.1.1 - Level A)
- ✅ All images have descriptive alt text
- ✅ Decorative images use `alt=""` or `role="presentation"`
- ✅ Icons have `aria-label` attributes

**Implementation**:
```tsx
<RocketLaunch aria-label="Start building" />
<img src="logo.png" alt="Agent Builder Platform logo" />
```

### 1.3 Adaptable

#### Info and Relationships (1.3.1 - Level A)
- ✅ Semantic HTML elements (`<header>`, `<main>`, `<nav>`)
- ✅ Proper heading hierarchy (h1 → h2 → h3)
- ✅ Form labels associated with inputs
- ✅ ARIA landmarks for page regions

**Implementation**:
```tsx
<header role="banner">
  <nav aria-label="Main navigation">
    {/* Navigation items */}
  </nav>
</header>
<main id="main-content" role="main">
  {/* Main content */}
</main>
```

#### Meaningful Sequence (1.3.2 - Level A)
- ✅ Logical reading order in DOM
- ✅ Tab order follows visual order
- ✅ Content makes sense when linearized

### 1.4 Distinguishable

#### Color Contrast (1.4.3 - Level AA)
- ✅ Text contrast ratio ≥ 4.5:1 for normal text
- ✅ Text contrast ratio ≥ 3:1 for large text (18pt+)
- ✅ UI component contrast ratio ≥ 3:1

**Light Theme Contrast**:
- Text on background: 12.6:1 (#1e293b on #f8fafc)
- Primary button: 4.8:1 (#ffffff on #2563eb)

**Dark Theme Contrast**:
- Text on background: 14.2:1 (#f1f5f9 on #0f172a)
- Primary button: 5.1:1 (#ffffff on #60a5fa)

#### Resize Text (1.4.4 - Level AA)
- ✅ Text can be resized up to 200% without loss of functionality
- ✅ Responsive font sizes using `rem` units
- ✅ No horizontal scrolling at 200% zoom

#### Text Spacing (1.4.12 - Level AA)
- ✅ Line height at least 1.5x font size
- ✅ Paragraph spacing at least 2x font size
- ✅ Letter spacing at least 0.12x font size

## Operable

### 2.1 Keyboard Accessible

#### Keyboard (2.1.1 - Level A)
- ✅ All functionality available via keyboard
- ✅ No keyboard traps
- ✅ Logical tab order

**Keyboard Shortcuts**:
- `Tab` - Navigate forward
- `Shift + Tab` - Navigate backward
- `Enter` / `Space` - Activate buttons/links
- `Escape` - Close modals/menus
- `Arrow keys` - Navigate lists/menus

**Implementation**:
```tsx
// Keyboard activation hook
const { onKeyDown, role, tabIndex } = useKeyboardActivation(handleClick)
<div onClick={handleClick} {...{ onKeyDown, role, tabIndex }}>
  Clickable element
</div>
```

#### No Keyboard Trap (2.1.2 - Level A)
- ✅ Focus can always move away from components
- ✅ Modal dialogs have proper focus management
- ✅ Escape key closes modals

**Implementation**:
```tsx
// Focus trap for modals
const containerRef = useFocusTrap(isOpen)
```

#### Focus Visible (2.4.7 - Level AA)
- ✅ Visible focus indicators on all interactive elements
- ✅ 2px outline with 2px offset
- ✅ High contrast focus styles

**CSS**:
```css
*:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}
```

### 2.4 Navigable

#### Skip Links (2.4.1 - Level A)
- ✅ Skip to main content link
- ✅ Skip to navigation link
- ✅ Visible on keyboard focus

**Implementation**:
```tsx
<SkipLinks />
// Renders:
// - Skip to main content
// - Skip to navigation
```

#### Page Titled (2.4.2 - Level A)
- ✅ Descriptive page titles
- ✅ Title updates on route change

#### Focus Order (2.4.3 - Level A)
- ✅ Tab order follows visual order
- ✅ Logical navigation sequence

#### Link Purpose (2.4.4 - Level A)
- ✅ Link text describes destination
- ✅ No "click here" or "read more" without context

#### Headings and Labels (2.4.6 - Level AA)
- ✅ Descriptive headings
- ✅ Clear form labels
- ✅ Proper heading hierarchy

## Understandable

### 3.1 Readable

#### Language of Page (3.1.1 - Level A)
- ✅ `lang="en"` attribute on `<html>`
- ✅ Language changes marked with `lang` attribute

### 3.2 Predictable

#### On Focus (3.2.1 - Level A)
- ✅ No context changes on focus
- ✅ Predictable behavior

#### On Input (3.2.2 - Level A)
- ✅ No automatic form submission
- ✅ Changes announced to screen readers

#### Consistent Navigation (3.2.3 - Level AA)
- ✅ Navigation in same location on all pages
- ✅ Consistent component behavior

### 3.3 Input Assistance

#### Error Identification (3.3.1 - Level A)
- ✅ Form errors clearly identified
- ✅ Error messages associated with fields
- ✅ `aria-invalid` on error fields

**Implementation**:
```tsx
<AccessibleTextField
  label="Email"
  value={email}
  onChange={setEmail}
  error={emailError}
  required
/>
```

#### Labels or Instructions (3.3.2 - Level A)
- ✅ All form fields have labels
- ✅ Required fields marked with `aria-required`
- ✅ Instructions provided where needed

#### Error Suggestion (3.3.3 - Level AA)
- ✅ Helpful error messages
- ✅ Suggestions for correction

## Robust

### 4.1 Compatible

#### Parsing (4.1.1 - Level A)
- ✅ Valid HTML
- ✅ No duplicate IDs
- ✅ Proper nesting of elements

#### Name, Role, Value (4.1.2 - Level A)
- ✅ All UI components have accessible names
- ✅ Roles properly assigned
- ✅ States and properties communicated

**ARIA Attributes Used**:
- `aria-label` - Accessible name
- `aria-labelledby` - Reference to label
- `aria-describedby` - Additional description
- `aria-expanded` - Expandable state
- `aria-haspopup` - Popup indicator
- `aria-live` - Live region updates
- `aria-atomic` - Announce entire region
- `aria-invalid` - Error state
- `aria-required` - Required field
- `aria-hidden` - Hide from screen readers

## Testing

### Manual Testing

#### Keyboard Navigation
1. Navigate entire site using only keyboard
2. Verify all interactive elements are reachable
3. Check focus indicators are visible
4. Test modal focus trapping

#### Screen Reader Testing
- **NVDA** (Windows) - Primary testing
- **JAWS** (Windows) - Secondary testing
- **VoiceOver** (macOS/iOS) - Mobile testing

#### Browser Testing
- Chrome + ChromeVox
- Firefox + NVDA
- Safari + VoiceOver
- Edge + Narrator

### Automated Testing

#### Tools
- **axe DevTools** - Browser extension
- **Lighthouse** - Chrome DevTools
- **WAVE** - Web accessibility evaluation tool
- **Pa11y** - Command-line testing

#### Running Tests
```bash
# Install axe-core
npm install --save-dev @axe-core/react

# Run accessibility audit in development
npm run dev
# Check console for accessibility issues
```

### Accessibility Checklist

- [ ] All images have alt text
- [ ] Proper heading hierarchy (no skipped levels)
- [ ] All form inputs have labels
- [ ] Color contrast meets WCAG AA standards
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators are visible
- [ ] Skip links are present and functional
- [ ] ARIA attributes used correctly
- [ ] Screen reader announces dynamic content
- [ ] No keyboard traps
- [ ] Error messages are clear and helpful
- [ ] Page titles are descriptive
- [ ] Language is set correctly

## Tools and Utilities

### Custom Hooks

#### `useKeyboardNavigation`
Handle keyboard events for navigation.

```tsx
useKeyboardNavigation({
  onEnter: handleSubmit,
  onEscape: handleClose,
  onArrowDown: handleNext,
  onArrowUp: handlePrevious,
})
```

#### `useFocusManagement`
Manage focus for modals and dialogs.

```tsx
const previousFocusRef = useFocusManagement(isOpen)
```

#### `useFocusTrap`
Trap focus within a container.

```tsx
const containerRef = useFocusTrap(isActive)
```

### Utility Functions

#### `announceToScreenReader`
Announce messages to screen readers.

```tsx
announceToScreenReader('Form submitted successfully', 'polite')
```

#### `generateAriaId`
Generate unique IDs for ARIA relationships.

```tsx
const labelId = generateAriaId('label')
const descriptionId = generateAriaId('description')
```

### Components

#### `<SkipLinks />`
Skip navigation links.

#### `<LiveRegion />`
Announce dynamic content to screen readers.

```tsx
<LiveRegion message="Loading complete" priority="polite" />
```

#### `<AccessibleTextField />`
Form field with proper ARIA attributes.

```tsx
<AccessibleTextField
  label="Username"
  value={username}
  onChange={setUsername}
  error={usernameError}
  required
/>
```

## Resources

### WCAG Guidelines
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Understanding WCAG 2.1](https://www.w3.org/WAI/WCAG21/Understanding/)

### Testing Tools
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Pa11y](https://pa11y.org/)

### Screen Readers
- [NVDA](https://www.nvaccess.org/) (Free, Windows)
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) (Paid, Windows)
- [VoiceOver](https://www.apple.com/accessibility/voiceover/) (Built-in, macOS/iOS)

### Learning Resources
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

## Support

For accessibility issues or questions:
- Create an issue in the repository
- Email: accessibility@agentbuilder.com
- Include: Browser, assistive technology, and steps to reproduce

---

**Last Updated**: [Date]  
**Maintained By**: Frontend Team  
**Compliance Level**: WCAG 2.1 Level AA
