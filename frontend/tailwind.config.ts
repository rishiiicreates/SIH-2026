import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'bis-blue': '#1a365d',
        'bis-saffron': '#FF9933',
      }
    },
  },
  plugins: [],
}
export default config
