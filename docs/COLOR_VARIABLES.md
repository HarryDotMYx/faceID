# Color Variables and Constants

## TailwindCSS Configuration

These color configurations are defined in `tailwind.config.js`:

```javascript
colors: {
    transparent: 'transparent',
    current: 'currentColor',
    
    // Primary Colors
    blue: {
        50:  '#EFF6FF',
        100: '#DBEAFE',
        200: '#BFDBFE',
        300: '#93C5FD',
        400: '#60A5FA',
        500: '#3B82F6',
        600: '#2563EB',
        700: '#1D4ED8',
        800: '#1E40AF',
        900: '#1E3A8A',
    },
    
    // Success Colors
    green: {
        50:  '#F0FDF4',
        100: '#DCFCE7',
        200: '#BBF7D0',
        300: '#86EFAC',
        400: '#4ADE80',
        500: '#22C55E',
        600: '#16A34A',
        700: '#15803D',
        800: '#166534',
        900: '#14532D',
    },
    
    // Error Colors
    red: {
        50:  '#FEF2F2',
        100: '#FEE2E2',
        200: '#FECACA',
        300: '#FCA5A5',
        400: '#F87171',
        500: '#EF4444',
        600: '#DC2626',
        700: '#B91C1C',
        800: '#991B1B',
        900: '#7F1D1D',
    },
    
    // Warning Colors
    yellow: {
        50:  '#FEFCE8',
        100: '#FEF9C3',
        200: '#FEF08A',
        300: '#FDE047',
        400: '#FACC15',
        500: '#EAB308',
        600: '#CA8A04',
        700: '#A16207',
        800: '#854D0E',
        900: '#713F12',
    },
    
    // Neutral Colors
    gray: {
        50:  '#F9FAFB',
        100: '#F3F4F6',
        200: '#E5E7EB',
        300: '#D1D5DB',
        400: '#9CA3AF',
        500: '#6B7280',
        600: '#4B5563',
        700: '#374151',
        800: '#1F2937',
        900: '#111827',
    },
    
    // Theme-specific Colors
    dark: {
        DEFAULT: '#1a1a1a',
        50: '#2a2a2a',
        100: '#3a3a3a',
        200: '#4a4a4a',
        300: '#5a5a5a',
        400: '#6a6a6a',
        500: '#7a7a7a',
        600: '#8a8a8a',
        700: '#9a9a9a',
        800: '#aaaaaa',
        900: '#bababa',
    },
}
```

## CSS Custom Properties

These variables are available globally through CSS custom properties:

```css
:root {
    /* Primary Colors */
    --color-primary: #3B82F6;
    --color-primary-light: #60A5FA;
    --color-primary-dark: #2563EB;
    
    /* Success Colors */
    --color-success: #22C55E;
    --color-success-light: #4ADE80;
    --color-success-dark: #16A34A;
    
    /* Error Colors */
    --color-error: #EF4444;
    --color-error-light: #F87171;
    --color-error-dark: #DC2626;
    
    /* Warning Colors */
    --color-warning: #EAB308;
    --color-warning-light: #FACC15;
    --color-warning-dark: #CA8A04;
    
    /* Neutral Colors */
    --color-text: #374151;
    --color-text-light: #6B7280;
    --color-text-dark: #1F2937;
    
    /* Background Colors */
    --color-background: #FFFFFF;
    --color-background-alt: #F9FAFB;
    --color-background-dark: #111827;
}

/* Dark Theme Variables */
[data-theme="dark"] {
    --color-text: #F9FAFB;
    --color-text-light: #D1D5DB;
    --color-text-dark: #F3F4F6;
    
    --color-background: #111827;
    --color-background-alt: #1F2937;
    --color-background-dark: #374151;
}
```

## Usage Examples

### JavaScript Theme Switching

```javascript
// In theme.js
const setTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('theme', theme);
};

// Apply theme based on user preference
const userTheme = localStorage.getItem('theme') || 'light';
setTheme(userTheme);
```

### React Components

```javascript
// Example button component using Tailwind classes
const Button = ({ variant = 'primary', children }) => {
    const variants = {
        primary: 'bg-blue-500 hover:bg-blue-600',
        success: 'bg-green-500 hover:bg-green-600',
        error: 'bg-red-500 hover:bg-red-600',
        warning: 'bg-yellow-500 hover:bg-yellow-600',
    };
    
    return (
        <button className={`${variants[variant]} text-white px-4 py-2 rounded`}>
            {children}
        </button>
    );
};
```

### Django Templates

```html
<!-- Example alert component -->
{% if messages %}
    {% for message in messages %}
        <div class="{% if message.tags == 'error' %}
                    bg-red-50 border-red-400 text-red-700
                   {% elif message.tags == 'success' %}
                    bg-green-50 border-green-400 text-green-700
                   {% elif message.tags == 'warning' %}
                    bg-yellow-50 border-yellow-400 text-yellow-700
                   {% else %}
                    bg-blue-50 border-blue-400 text-blue-700
                   {% endif %}
                   px-4 py-3 rounded relative border"
             role="alert">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## Best Practices

1. **Consistency**
   - Use the predefined color scales consistently throughout the application
   - Avoid using arbitrary color values
   - Stick to the semantic meaning of colors

2. **Accessibility**
   - Ensure sufficient contrast ratios (minimum 4.5:1 for normal text)
   - Don't rely solely on color to convey information
   - Test with color blindness simulators

3. **Theme Support**
   - Use CSS custom properties for theme-dependent colors
   - Provide dark mode alternatives for all color combinations
   - Test both light and dark themes thoroughly

4. **Maintenance**
   - Document any new color additions
   - Update this documentation when making color system changes
   - Keep color naming consistent with the established pattern