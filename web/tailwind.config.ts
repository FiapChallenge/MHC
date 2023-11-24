import type { Config } from "tailwindcss";

const plugin = require("tailwindcss/plugin");

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      textShadow: {
        DEFAULT:
          "1px 1px 2px #000000, 1px 1px 2px #000000, 1px 1px 2px #000000;",
      },
      colors: {
        text: {
          DEFAULT: "#222222",
          50: "#f2f2f2",
          100: "#e6e6e6",
          200: "#cccccc",
          300: "#b3b3b3",
          400: "#999999",
          500: "#808080",
          600: "#666666",
          700: "#4d4d4d",
          800: "#333333",
          900: "#1a1a1a",
          950: "#0d0d0d",
        },
        background: {
          DEFAULT: "#ffffff",
          50: "#fafafa",
          100: "#e6e6e6",
          200: "#cccccc",
          300: "#b3b3b3",
          400: "#999999",
          500: "#808080",
          600: "#666666",
          700: "#4d4d4d",
          800: "#333333",
          900: "#1a1a1a",
          950: "#0d0d0d",
        },
        primary: {
          DEFAULT: "#43c7c7",
          50: "#ebf9f9",
          100: "#d8f3f3",
          200: "#b0e8e8",
          300: "#89dcdc",
          400: "#62d0d0",
          500: "#3bc4c4",
          600: "#2f9d9d",
          700: "#237676",
          800: "#174f4f",
          900: "#0c2727",
          950: "#061414",
        },
        secondary: {
          DEFAULT: "#d8e6f3",
          50: "#ebf2f9",
          100: "#d8e6f3",
          200: "#b1cde7",
          300: "#8ab4db",
          400: "#639bcf",
          500: "#3c82c3",
          600: "#30689c",
          700: "#244e75",
          800: "#18344e",
          900: "#0c1a27",
          950: "#060d14",
        },
        accent: {
          DEFAULT: "#3bc480",
          50: "#ebf9f2",
          100: "#d8f3e6",
          200: "#b0e8cc",
          300: "#89dcb3",
          400: "#62d099",
          500: "#3bc480",
          600: "#2f9d66",
          700: "#23764d",
          800: "#174f33",
          900: "#0c271a",
          950: "#06140d",
        },
      },
      screens: {
        xs: "375px",
      },
      fontSize: {
        sm: "0.750rem",
        md: "0.875rem",
        base: "1rem",
        xl: "1.333rem",
        "2xl": "1.777rem",
        "3xl": "2.369rem",
        "4xl": "3.158rem",
        "5xl": "4.210rem",
      },
      fontFamily: {
        heading: ["var(--font-montserrat)"],
        body: ["var(--font-poppins)"],
      },
      fontWeight: {
        normal: "400",
        bold: "700",
      },
      animation: {
        "spin-slow": "spin 3s linear infinite",
      },
    },
  },
  plugins: [],
};
export default config;
