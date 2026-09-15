/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0B1F33",
        slate: "#334155",
        offwhite: "#F8FAFC",
        accent: "#2563EB",
        cyan: "#0891B2",
        amber: "#D97706",
        critical: "#DC2626",
      },
      fontFamily: {
        sans: ["Inter", "IBM Plex Sans", "Manrope", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
