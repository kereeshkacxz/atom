// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false, // Отключение серверного рендеринга (SPA)
  devtools: { enabled: true }, // Включение инструментов разработчика для удобства

  css: ["~/assets/css/main.css"], // Подключение основного CSS файла

  vite: {
    server: {
      watch: {
        usePolling: true, // Использование polling для отслеживания изменений (полезно в Docker)
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
      backendUrl: process.env.BACKEND_URL || "http://localhost:8080", // URL бэкенда
      pages: {
        about: "О сервисе", // Название страницы "О сервисе"
      },
    },
  },

  components: [
    {
      path: "~/components",
      pathPrefix: false, // Отключение префикса пути для компонентов
    },
  ],

  compatibilityDate: "2024-08-14", // Дата совместимости
  modules: ["@nuxt/image"], // Подключение модуля для работы с изображениями
});
