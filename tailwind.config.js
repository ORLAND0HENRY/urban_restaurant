/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py', // Include Django files for dynamic class usage
  ],
  theme: {
    extend: {
      colors: {
        'up-light': '#fefefe',    // Elegant light tone
        'up-primary': '#a18357',  // Subtle dark accent (Earthy Gold/Brown)
        'up-secondary': '#333333', // Deep charcoal for text/dark accents
        'up-background': '#f5f5f5', // Very light grey for background
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'], // Modern clean sans-serif
        'serif': ['Playfair Display', 'serif'], // Elegant heading font
      },
      boxShadow: {
        'soft': '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}