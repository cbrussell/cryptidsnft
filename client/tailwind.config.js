module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cryptid-1': '#f6d5c0',
        'cryptid-2': '#f5c59f',
        'cryptid-3': '#ee9681',
        'cryptid-4': '#d27a6f',
        'cryptid-5': '#222222',
        'cryptid-6': '#B25E54',
        },
        fontFamily: {
          "YkarRegular" : ["YKAR Medium", "sans-serif"],
          "Exo" : ["Exo", "sans-serif"],
        }
       
      },
    
  },
  variants: {
    fill: ['hover', 'focus'], // this line does the trick
  },
  plugins: [],
}
