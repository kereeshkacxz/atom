// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false, // Отключение серверного рендеринга (SPA)
  devtools: { enabled: false }, // Включение инструментов разработчика для удобства

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
      title: "Atom", // Заголовок страницы
      meta: [
        {
          name: "description",
          content:
            "Automation of requirements verification in a certified circuit",
        }, // Мета-тег описания
        { name: "viewport", content: "width=device-width, initial-scale=1" }, // Мета-тег для адаптивности
        { name: "keywords", content: "nuxt, vue, app, web-development" }, // Мета-тег ключевых слов
      ],
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
        {
          rel: "icon",
          type: "image/x-icon",
          href: "/favicon.ico",
        },
      ],
    },
  },

  runtimeConfig: {
    public: {
      backendUrl:
        `http://${process.env.BACKEND_HOST}:${process.env.BACKEND_PORT}` ||
        "http://localhost:8080", // URL бэкенда
      pages: {},
    },
  },

  components: [
    {
      path: "~/components",
      pathPrefix: false, // Отключение префикса пути для компонентов
    },
  ],

  compatibilityDate: "2024-08-14", // Дата совместимости
  modules: ["@nuxt/image"],
  image: { dir: "public" }, // Подключение модуля для работы с изображениями
});
