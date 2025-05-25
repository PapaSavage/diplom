// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },

  css: ["~/assets/css/main.css", "~/assets/css/base.scss"],
  vite: {
    plugins: [tailwindcss()],
  },

  app: {
    head: {
      title: "МедВизор",

      meta: [
        { charset: "utf-8" },

        { name: "viewport", content: "width=device-width, initial-scale=1" },
      ],

      link: [{ rel: "icon", type: "image/svg", href: "/favicon.svg" }],
    },
    layoutTransition: { name: "layout", mode: "out-in" },
    pageTransition: { name: "page", mode: "out-in" },
  },

  devServer: {
    port: 3002, // Укажите желаемый порт здесь
  },

  modules: ["shadcn-nuxt", "@nuxt/eslint", "@nuxt/fonts", "nuxt-auth-sanctum"],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: "",
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: "./components/ui",
  },

  fonts: {
    families: [{ name: "Inter", provider: "google" }],
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URl,
    },
  },

  sanctum: {
    baseUrl: "http://127.0.0.1:8000", // Laravel API

    mode: "token",

    endpoints: {
      login: "/api/login",
      logout: "/api/logout",
    },

    redirect: {
      onAuthOnly: "/login",
      onGuestOnly: "/diagnostics",
      // onLogin: "/diagnostics",
    },
    globalMiddleware: {
      enabled: true,
    },
  },
});
