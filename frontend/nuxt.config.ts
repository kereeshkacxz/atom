// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: false },
  css: ["~/assets/css/main.css"],

  vite: {
    server: {
      watch: {
        usePolling: true,
      },
    },
  },

  app: {
    head: {
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans:ital,wght@0,100..900;1,100..900&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans:ital,wght@0,100..900;1,100..900&family=Rubik+Wet+Paint&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Anton&display=swap",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap",
        },
      ],
    },
  },

  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || "http://localhost:8080",
      pages: {
        about: "О сервисе",
      },
    },
  },

  components: [
    {
      path: "~/components",
      pathPrefix: false,
    },
  ],

  compatibilityDate: "2024-08-14",
  modules: ["@nuxt/image"],
});
