/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Update this path as needed
    './static/**/*.js',      // If you have JS files that use Tailwind
    './static/css/**/*.css',  // If you have additional CSS files that use Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms'),],
};
