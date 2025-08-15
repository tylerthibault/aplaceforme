# Design System Documentation

## Overview
This project has been modernized with a Apple-inspired glassmorphism design system that replaces heavy linear gradients with subtle glass effects, system fonts, and refined shadows.

## Design Tokens (`src/static/css/tokens.css`)

### Color System
The design uses a restrained color palette based on modern iOS/macOS patterns:

- **Primary Colors**: Neutral backgrounds and glass surfaces
- **Text Colors**: High contrast primary, medium secondary, low tertiary
- **Accent Colors**: iOS-inspired blues, with limited use for CTAs
- **Brand Colors**: Maintains existing faith-inspired gold and blue elements

### Glassmorphism Variables
Glass effects are controlled by CSS custom properties:
- `--glass-alpha-*`: Transparency levels (light/medium/heavy)
- `--glass-blur-*`: Blur amounts (8px/12px/20px)
- `--glass-bg-*`: Pre-configured glass backgrounds with fallbacks

### Shadow System
Layered shadow system with 4 elevation levels:
- `--shadow-elevation-1`: Subtle card shadows
- `--shadow-elevation-2`: Standard component shadows  
- `--shadow-elevation-3`: Elevated/hover shadows
- `--shadow-elevation-4`: Modal/popup shadows

### Typography
Modern system font stack:
- `--font-system`: SF Pro Display/Helvetica for headings
- `--font-system-body`: SF Pro Text/Helvetica for body text
- Typography scale: `--text-xs` to `--text-5xl`

## Utility Classes (`src/static/css/glassmorphism.css`)

### Glass Effects
- `.glass` - Light glass surface with backdrop-filter
- `.glass-medium` - Medium opacity glass surface  
- `.glass-heavy` - High opacity glass surface
- `.glass-dark` - Dark glass for light text on dark backgrounds

### Shadow Effects
- `.soft-shadow-sm` to `.soft-shadow-xl` - Graduated shadow system
- `.soft-shadow-hover` - Hover state animations

### Modern Buttons
- `.accent-btn` - Primary iOS-style button with shadow and transform
- `.accent-btn-secondary` - Glass button with subtle styling
- Size variants: `.accent-btn-sm`, `.accent-btn-lg`

### Cards & Surfaces
- `.modern-card` - Glass card with hover effects and transitions
- `.surface` - Basic glass surface 
- `.surface-elevated` - Elevated surface with shadows

## Component Updates

### Hero Sections
- Replaced heavy cream/white gradients with subtle radial highlights
- Updated to use system typography and modern spacing
- Background uses `--highlight-brand` for subtle color variation

### Feature Cards  
- Converted to glassmorphism with backdrop-filter
- Added hover animations and soft shadows
- Icons use glass backgrounds instead of gradients

### Buttons
- Primary buttons use iOS blue (`--color-accent-primary`)
- Secondary buttons use glass effects with border accents
- Hover states include transform and shadow changes

### Navigation & Branding
- Brand text uses accent color with subtle underline
- Removed text gradient clipping for better accessibility

## Browser Support & Fallbacks

### Backdrop Filter Fallbacks
All glass effects include `@supports not (backdrop-filter: blur())` fallbacks:
- Glass backgrounds fallback to slightly more opaque solid colors
- Ensures visual consistency across browsers

### Color Mix Fallback
Button hover states use `color-mix()` with automatic fallbacks for older browsers.

## Usage Guidelines

### Do's
- Use `.glass` classes for cards and surfaces that need translucency
- Apply `.soft-shadow-*` for depth instead of harsh borders
- Use `.accent-btn` for primary actions, `.accent-btn-secondary` for secondary
- Leverage CSS custom properties for consistent theming

### Don'ts  
- Avoid multiple glass layers that reduce readability
- Don't use heavy gradients - prefer subtle highlights
- Minimize accent color usage - keep it for important CTAs only
- Don't override typography scale - use the defined `--text-*` values

## Customization

### Changing Colors
Update values in `:root` of `tokens.css`:
```css
:root {
    --color-accent-primary: #007AFF; /* Change primary accent */
    --glass-alpha-light: 0.8;        /* Adjust glass opacity */
}
```

### Dark Mode
Dark mode variables are automatically applied via `@media (prefers-color-scheme: dark)`.

### Animation Preferences
Respects `prefers-reduced-motion` for accessibility.

## Migration Notes

### Replaced Gradients
- Hero section: `linear-gradient(135deg, cream, white)` → subtle radial highlights
- Feature icons: `linear-gradient(135deg, cream, white)` → glass backgrounds  
- Brand text: gradient text clipping → accent color with underline
- Community section: blue gradient → glass surface with highlight
- Admin sidebar: dark gradient → dark glass with blur

### Updated Components
- All buttons now use modern styling with transforms and shadows
- Cards use glassmorphism instead of solid backgrounds
- Typography switched to system font stack
- Spacing updated to 8pt grid system (`--space-*`)

The design maintains the faith-inspired visual identity while providing a more modern, accessible, and maintainable foundation.