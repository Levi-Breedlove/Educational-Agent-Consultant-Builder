# Node.js-Inspired Dark Theme Guide

## Overview
The Agent Builder Platform now features a beautiful Node.js-inspired dark theme with glassmorphism effects, animated gradients, and Node.js green accent colors.

## Theme Colors

### Node.js Green Palette
```css
Primary Green: #68d391 (Node.js inspired)
Light Green:   #9ae6b4
Dark Green:    #48bb78
Darker Green:  #38a169
```

### Complementary Colors
```css
Blue Accent:   #4299e1
Purple Accent: #8b5cf6
```

### Background Colors
```css
Deep Dark:     #0a0e1a (Base background)
Dark Blue:     #1a1f35 (Gradient accent)
Glass Paper:   rgba(15, 23, 42, 0.7) (Glassmorphism)
```

## Key Features

### 1. Animated Gradient Background
The dark mode features a subtle animated gradient that shifts over 15 seconds:
- Creates depth and visual interest
- Smooth transitions between dark blue tones
- Non-distracting animation speed

### 2. Glassmorphism Effects
All Paper components in dark mode use glassmorphism:
- **Backdrop Blur**: 20px blur with 180% saturation
- **Transparency**: 70% opacity for depth
- **Border**: Subtle rgba borders for definition
- **Glow**: Node.js green glow on elevation

### 3. Radial Gradient Overlays
Three radial gradients create ambient lighting:
- **Green** (20%, 30%): Node.js brand color
- **Blue** (80%, 70%): Complementary accent
- **Purple** (50%, 50%): Center highlight

### 4. Node.js Green Accents
Strategic use of Node.js green throughout:
- Primary buttons with gradient
- Progress bars with glow effect
- Active phase indicators
- Icon highlights
- Text gradients in headers

## Component Enhancements

### HomePage
```tsx
// Gradient text title
background: 'linear-gradient(135deg, #68d391 0%, #4299e1 100%)'
WebkitBackgroundClip: 'text'
WebkitTextFillColor: 'transparent'

// Glassmorphism card
background: 'rgba(15, 23, 42, 0.7)'
backdropFilter: 'blur(20px) saturate(180%)'
border: '1px solid rgba(104, 211, 145, 0.2)'

// Hover effects
'&:hover': {
  transform: 'translateY(-4px)',
  boxShadow: '0 8px 24px rgba(104, 211, 145, 0.2)',
  border: '1px solid rgba(104, 211, 145, 0.3)',
}
```

### Layout (AppBar)
```tsx
// Glass navigation bar
background: 'rgba(15, 23, 42, 0.8)'
backdropFilter: 'blur(20px) saturate(180%)'
borderBottom: '1px solid rgba(104, 211, 145, 0.2)'
boxShadow: '0 4px 20px rgba(104, 211, 145, 0.1)'

// Gradient title
background: 'linear-gradient(135deg, #68d391 0%, #4299e1 100%)'
WebkitBackgroundClip: 'text'
WebkitTextFillColor: 'transparent'

// Icon glow
filter: 'drop-shadow(0 0 8px rgba(104, 211, 145, 0.5))'
```

### ProgressTracker
```tsx
// Node.js green progress bar
background: 'linear-gradient(90deg, #68d391 0%, #48bb78 100%)'
boxShadow: '0 0 10px rgba(104, 211, 145, 0.5)'

// Active phase indicator
backgroundColor: '#68d391'
boxShadow: '0 0 8px rgba(104, 211, 145, 0.6)'

// Active phase card
borderColor: '#68d391'
backgroundColor: 'rgba(104, 211, 145, 0.1)'
boxShadow: '0 4px 12px rgba(104, 211, 145, 0.2)'

// Icon glow
filter: 'drop-shadow(0 0 4px rgba(104, 211, 145, 0.5))'
```

### Buttons
```tsx
// Primary button gradient
background: 'linear-gradient(135deg, #68d391 0%, #48bb78 100%)'
color: '#000' // Black text for contrast
fontWeight: 600
boxShadow: '0 4px 20px rgba(104, 211, 145, 0.4)'

// Hover state
'&:hover': {
  background: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)',
  boxShadow: '0 6px 30px rgba(104, 211, 145, 0.6)',
  transform: 'translateY(-2px)',
}
```

## CSS Utilities

### Glassmorphism Classes
```css
.glass {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.glass-light {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(0, 0, 0, 0.1);
}
```

### Glow Effects
```css
.node-glow {
  box-shadow: 0 0 20px rgba(104, 211, 145, 0.15);
}

.node-glow-strong {
  box-shadow: 0 0 40px rgba(104, 211, 145, 0.25);
}
```

### Scrollbar Styling
```css
body[data-theme="dark"] ::-webkit-scrollbar-thumb {
  background: rgba(104, 211, 145, 0.2);
  border-radius: 4px;
}

body[data-theme="dark"] ::-webkit-scrollbar-thumb:hover {
  background: rgba(104, 211, 145, 0.4);
}
```

## Animation Details

### Gradient Shift
```css
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Applied to body */
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
```

### Component Transitions
```tsx
// Standard transition for interactive elements
transition: 'all 0.3s ease-in-out'

// Transform on hover
transform: 'translateY(-2px)' // Lift effect
transform: 'scale(1.02)'      // Subtle scale
```

## Theme Toggle

The theme automatically:
1. Sets `data-theme` attribute on `<body>`
2. Applies CSS custom properties
3. Updates MUI theme context
4. Persists user preference

```tsx
// In Layout component
useEffect(() => {
  document.body.setAttribute('data-theme', currentTheme)
}, [currentTheme])
```

## Browser Support

### Backdrop Filter
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support (v103+)
- Safari: ✅ Full support (with -webkit prefix)

### CSS Gradients
- All modern browsers: ✅ Full support

### CSS Animations
- All modern browsers: ✅ Full support

## Performance Considerations

### Optimizations
1. **GPU Acceleration**: Transform and opacity animations use GPU
2. **Will-Change**: Applied to animated elements
3. **Backdrop Filter**: Hardware accelerated on supported devices
4. **Gradient Animation**: Smooth 15s duration prevents jank

### Best Practices
- Avoid animating expensive properties (width, height)
- Use transform and opacity for animations
- Limit backdrop-filter to necessary elements
- Use CSS containment where appropriate

## Accessibility

### Contrast Ratios
- Node.js green (#68d391) on dark: ✅ WCAG AA compliant
- Text on glass backgrounds: ✅ Enhanced with borders
- Focus indicators: ✅ High contrast outlines

### Reduced Motion
Consider adding:
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Design Philosophy

### Node.js Brand Alignment
- **Green**: Primary brand color, used for success and progress
- **Dark**: Professional, developer-focused aesthetic
- **Glass**: Modern, cutting-edge technology feel
- **Glow**: Subtle energy and activity indicators

### Visual Hierarchy
1. **Primary Actions**: Node.js green gradient buttons
2. **Active States**: Green borders and glows
3. **Progress**: Green progress bars with animation
4. **Completed**: Green checkmarks with glow
5. **Background**: Subtle, non-distracting gradients

### User Experience
- **Depth**: Glassmorphism creates layered interface
- **Focus**: Green accents guide attention
- **Feedback**: Hover states and transitions
- **Consistency**: Unified color palette throughout

## Future Enhancements

### Potential Additions
- [ ] Particle effects on background
- [ ] More pronounced glow on active elements
- [ ] Animated Node.js logo in corner
- [ ] Theme customization options
- [ ] Additional color schemes (React blue, Vue green, etc.)
- [ ] Dark mode intensity slider
- [ ] Custom accent color picker

## Code Examples

### Creating a Glass Card
```tsx
<Paper
  sx={{
    background: 'rgba(15, 23, 42, 0.7)',
    backdropFilter: 'blur(20px) saturate(180%)',
    border: '1px solid rgba(104, 211, 145, 0.2)',
    boxShadow: '0 8px 32px rgba(104, 211, 145, 0.15)',
    transition: 'all 0.3s ease',
    '&:hover': {
      boxShadow: '0 12px 48px rgba(104, 211, 145, 0.25)',
      transform: 'translateY(-2px)',
    },
  }}
>
  {/* Content */}
</Paper>
```

### Adding Node.js Glow
```tsx
<Box
  sx={{
    color: '#68d391',
    filter: 'drop-shadow(0 0 8px rgba(104, 211, 145, 0.5))',
  }}
>
  <Icon />
</Box>
```

### Gradient Text
```tsx
<Typography
  sx={{
    background: 'linear-gradient(135deg, #68d391 0%, #4299e1 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  }}
>
  Gradient Text
</Typography>
```

## Testing Checklist

- [ ] Dark mode toggle works correctly
- [ ] Glassmorphism renders on all browsers
- [ ] Animations are smooth (60fps)
- [ ] Hover states provide feedback
- [ ] Text is readable on all backgrounds
- [ ] Focus indicators are visible
- [ ] Mobile responsive design works
- [ ] Theme persists across sessions
- [ ] No performance issues with animations
- [ ] Accessibility standards met

## Resources

- [Node.js Brand Guidelines](https://nodejs.org/en/about/branding)
- [Glassmorphism Design](https://uxdesign.cc/glassmorphism-in-user-interfaces-1f39bb1308c9)
- [CSS Backdrop Filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
- [Material-UI Theming](https://mui.com/material-ui/customization/theming/)
