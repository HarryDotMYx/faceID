module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
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
      },
    },
  },
  variants: {
    extend: {
      backgroundColor: ['dark'],
      borderColor: ['dark'],
      textColor: ['dark'],
    },
  },
  plugins: [],
}