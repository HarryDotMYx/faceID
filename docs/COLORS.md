# Color System Documentation

## Primary Colors

### Blue Variants
  css
/* Primary Blue - Used for main actions, links, and primary buttons */
bg-blue-500: #3B82F6  /* Default state */
bg-blue-600: #2563EB  /* Hover state */
bg-blue-700: #1D4ED8  /* Active state */
bg-blue-50:  #EFF6FF  /* Light background */
bg-blue-100: #DBEAFE  /* Subtle background */
  

### Green Variants
  css
/* Success Green - Used for success states, confirmations, and positive actions */
bg-green-500: #22C55E  /* Default state */
bg-green-600: #16A34A  /* Hover state */
bg-green-700: #15803D  /* Active state */
bg-green-50:  #F0FDF4  /* Light background */
bg-green-100: #DCFCE7  /* Subtle background */
  

### Red Variants
  css
/* Error Red - Used for errors, warnings, and destructive actions */
bg-red-500: #EF4444  /* Default state */
bg-red-600: #DC2626  /* Hover state */
bg-red-700: #B91C1C  /* Active state */
bg-red-50:  #FEF2F2  /* Light background */
bg-red-100: #FEE2E2  /* Subtle background */
  

### Yellow Variants
  css
/* Warning Yellow - Used for warnings and important notifications */
bg-yellow-500: #EAB308  /* Default state */
bg-yellow-600: #CA8A04  /* Hover state */
bg-yellow-700: #A16207  /* Active state */
bg-yellow-50:  #FEFCE8  /* Light background */
bg-yellow-100: #FEF9C3  /* Subtle background */
  

## Neutral Colors

### Gray Scale
  css
/* Used for text, backgrounds, and borders */
bg-gray-50:  #F9FAFB  /* Lightest background */
bg-gray-100: #F3F4F6  /* Light background */
bg-gray-200: #E5E7EB  /* Border color */
bg-gray-500: #6B7280  /* Muted text */
bg-gray-600: #4B5563  /* Secondary text */
bg-gray-700: #374151  /* Primary text */
bg-gray-800: #1F2937  /* Dark background */
bg-gray-900: #111827  /* Darkest background */
  

## Usage Guidelines

### Buttons

1. Primary Actions
  html
<button class="bg-blue-500 hover:bg-blue-600 text-white">
    Primary Action
</button>
  

2. Success Actions
  html
<button class="bg-green-500 hover:bg-green-600 text-white">
    Confirm Action
</button>
  

3. Destructive Actions
  html
<button class="bg-red-500 hover:bg-red-600 text-white">
    Delete Action
</button>
  

4. Warning Actions
  html
<button class="bg-yellow-500 hover:bg-yellow-600 text-white">
    Warning Action
</button>
  

### Alerts and Messages

1. Success Message
  html
<div class="bg-green-50 border border-green-400 text-green-700">
    Success Message
</div>
  

2. Error Message
  html
<div class="bg-red-50 border border-red-400 text-red-700">
    Error Message
</div>
  

3. Warning Message
  html
<div class="bg-yellow-50 border border-yellow-400 text-yellow-700">
    Warning Message
</div>
  

4. Info Message
  html
<div class="bg-blue-50 border border-blue-400 text-blue-700">
    Info Message
</div>
  

### Face Recognition Status

1. Recognized Face
  html
<div class="border-green-400 bg-green-50">
    <span class="text-green-700">Recognized</span>
</div>
  

2. Unknown Face
  html
<div class="border-red-400 bg-red-50">
    <span class="text-red-700">Unknown</span>
</div>
  

### Theme Colors

1. Light Theme
  css
/* Background colors */
bg-white        /* Main background */
bg-gray-50      /* Secondary background */
bg-gray-100     /* Tertiary background */

/* Text colors */
text-gray-700   /* Primary text */
text-gray-600   /* Secondary text */
text-gray-500   /* Muted text */
  

2. Dark Theme
  css
/* Background colors */
bg-gray-900     /* Main background */
bg-gray-800     /* Secondary background */
bg-gray-700     /* Tertiary background */

/* Text colors */
text-white      /* Primary text */
text-gray-200   /* Secondary text */
text-gray-300   /* Muted text */
  

## Accessibility

- All color combinations meet WCAG 2.1 AA standards for contrast
- Text colors are chosen to ensure readability on their respective backgrounds
- Interactive elements have distinct hover and focus states
- Error states use colors AND icons/text to convey meaning (not just color alone)

## Implementation Notes

1. Always use the semantic color classes rather than arbitrary colors
2. Include hover states for interactive elements
3. Use lighter backgrounds (50, 100) for large surfaces
4. Use darker colors (600, 700) for text on light backgrounds
5. Ensure sufficient contrast between text and background colors