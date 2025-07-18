# CSS Architecture Documentation

## Overview
The CSS has been refactored from a single large file into a modular, maintainable architecture. This approach follows modern CSS organization principles and makes the codebase easier to maintain, debug, and extend.

## File Structure

```
src/static/css/
├── main-modular.css         # Main entry point (imports all modules)
├── main.css                 # Original monolithic file (for reference)
├── base/
│   ├── reset.css           # CSS reset and base styles
│   ├── variables.css       # CSS custom properties (variables)
│   └── typography.css      # Typography styles and utilities
├── layout/
│   └── grid.css           # Grid system and layout utilities
├── components/
│   ├── buttons.css        # Button components and variants
│   ├── cards.css          # Card components
│   ├── forms.css          # Form elements and validation
│   ├── navigation.css     # Navigation and menu styles
│   ├── hero.css           # Hero section and parallax effects
│   └── footer.css         # Footer styles
└── utils/
    ├── utilities.css      # Utility classes (spacing, display, etc.)
    └── responsive.css     # Responsive design utilities
```

## Architecture Principles

### 1. Base Layer
- **Reset**: Normalizes browser defaults
- **Variables**: Centralized design tokens (colors, spacing, typography)
- **Typography**: Base text styles and typographic utilities

### 2. Layout Layer
- **Grid**: Flexbox and CSS Grid utilities
- **Container**: Width constraints and padding

### 3. Components Layer
- **Modular**: Each component in its own file
- **Reusable**: Components can be used across pages
- **Maintainable**: Easy to find and modify specific component styles

### 4. Utilities Layer
- **Utilities**: Single-purpose classes for quick styling
- **Responsive**: Mobile-first responsive utilities

## Usage

### To use the modular CSS:
1. Update your HTML templates to reference `main-modular.css` instead of `main.css`
2. The import order in `main-modular.css` ensures proper cascade

### Example template update:
```html
<!-- Replace this -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">

<!-- With this -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main-modular.css') }}">
```

## Benefits

### 1. Maintainability
- Easy to locate styles for specific components
- Changes to one component don't affect others
- Clear separation of concerns

### 2. Performance
- Smaller individual files are easier to cache
- Can selectively import only needed components
- Better for development workflow

### 3. Scalability
- New components can be added without modifying existing files
- Team members can work on different components simultaneously
- Consistent organization as the project grows

### 4. Debugging
- Easier to find the source of styles
- Less CSS specificity conflicts
- Clear naming conventions

## Adding New Components

### 1. Create a new component file:
```css
/* components/my-component.css */
.my-component {
    /* styles here */
}

.my-component__element {
    /* BEM naming convention */
}

.my-component--variant {
    /* component variants */
}
```

### 2. Import in main-modular.css:
```css
@import url('./components/my-component.css');
```

## Design Tokens (CSS Variables)

All design tokens are centralized in `base/variables.css`:

- **Colors**: Primary, secondary, accent colors
- **Typography**: Font families and scales
- **Spacing**: Consistent spacing scale
- **Shadows**: Box shadow variations
- **Transitions**: Animation timing
- **Border Radius**: Consistent rounding

## Responsive Design

The architecture uses a mobile-first approach:

- Base styles apply to all screen sizes
- `sm`: Small screens (max-width: 640px)
- `md`: Medium screens (641px - 1024px)
- `lg`: Large screens (min-width: 1025px)

## Migration Notes

The original `main.css` file has been preserved for reference. The modular CSS provides the same functionality but with better organization.

Key improvements:
- Better file organization
- Clearer component boundaries
- Easier maintenance and debugging
- More scalable architecture
- Consistent naming conventions

## Future Enhancements

Potential additions to the architecture:
- Page-specific stylesheets (admin.css, auth.css)
- Theme variations
- Animation library
- Component documentation
- Automated CSS optimization
