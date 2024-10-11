<template>
  <div class="header_wrapper">
    <div class="div_navbar" :class="{ open: isMenuOpen }">
      <NuxtLink
        v-for="(key, i) in Object.keys(pages)"
        :key="i"
        class="btn_page"
        :class="{ active_page: useRoute().name.split('-')[0] === key }"
        :to="`/${key}`"
      >
        {{
          key !== "admin" || type === "admin" || type === "superadmin"
            ? pages[key]
            : ""
        }}
      </NuxtLink>
    </div>
    <div v-if="login !== ''" class="dropdown">
      <button class="dropbtn">Профиль</button>
      <div class="dropdown-content">
        <NuxtLink class="btn_page" to="/profile">Личная информация</NuxtLink>
        <a href="#">Link 2</a>
        <NuxtLink class="div_login btn_page" @click="logout()">Выйти</NuxtLink>
      </div>
    </div>
    <NuxtLink
      v-else
      class="div_autho btn_page"
      :style="{ width: '130px' }"
      :to="`/authorization`"
    >
      <img class="img" src="~/public/people.png" />
      Войти
    </NuxtLink>
    <div class="burger" @click="toggleMenu">
      <span></span>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const config = useRuntimeConfig();
const pages = config.public.pages;
const login = ref(" ");
const isMenuOpen = ref(false);
const type = ref("");
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
  const burgerElement = document.querySelector(".burger");
  if (burgerElement) {
    burgerElement.classList.toggle("active", isMenuOpen.value);
  }
};

const handleResize = () => {
  if (window.innerWidth > 1000 && isMenuOpen.value) {
    isMenuOpen.value = false;
    const burgerElement = document.querySelector(".burger");
    if (burgerElement) {
      burgerElement.classList.remove("active");
    }
  }
};

async function fetchData() {
  if (localStorage.getItem("token") === null) {
    login.value = "";
    return;
  }
  // try {
  //   const response = await $api.get(`api/v1/user/me`, {
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: `Bearer ${localStorage.getItem("token")}`,
  //     },
  //   });
  //   login.value = response.data.username;
  //   if (response.data.type === "admin") localStorage.setItem("admin", true);
  //   if (response.data.type === "superadmin")
  //     localStorage.setItem("superadmin", true);
  //   type.value = response.data.type;
  // } catch (error) {
  //   console.error(error);
  //   logout();
  // }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("admin");
  login.value = "";
  type.value = "";
}

onMounted(() => {
  fetchData();
  window.addEventListener("resize", handleResize);
  window.addEventListener("storage", (event) => {
    if (event.key === "token") {
      fetchData();
    }
  });
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.header_wrapper {
  z-index: 10;
  background-color: var(--bg-color);
  position: fixed;
  display: flex;
  width: 100%;
  height: var(--header-height);
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  user-select: none;
  border-bottom: 1px solid var(--main-color);
}
.burger {
  display: none;
  width: 32px;
  height: 32px;
  cursor: pointer;
  z-index: 1;
  position: relative;
}

.burger span {
  width: 100%;
  height: 4px;
  background-color: var(--main-color);
  border-radius: 12px;
  display: block;
  margin: auto;
  transition: background-color 0.2s ease-in-out;
}

.burger span::before,
.burger span::after {
  content: "";
  width: 100%;
  background-color: var(--main-color);
  display: block;
  transition: all 0.2s ease-in-out;
  border-radius: 12px;
  height: 4px;
}

.burger span::before {
  transform: translateY(-10px);
}

.burger span::after {
  transform: translateY(10px);
  margin-top: -4px;
}

.burger.active span {
  background-color: transparent;
}

.burger.active span::before {
  transform: rotateZ(45deg) translateY(0);
}

.burger.active span::after {
  transform: rotateZ(-45deg) translateY(0);
}

.div_navbar {
  display: flex;
  gap: 30px;
}

.div_navbar.open {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column;
  position: absolute;
  top: 70px;
  left: 0;
  right: 0;
  background-color: var(--bg-color);
  z-index: 1;
  width: 100%;
}
.div_login {
  text-align: center;
}
@media (max-width: 1080px) {
  .div_navbar {
    display: none;
  }
  .burger {
    display: flex;
  }

  .header_wrapper {
    display: flex;
    gap: 10px;
    justify-content: space-between;
    align-items: center;
  }

  .header_wrapper > :first-child {
    margin-right: auto;
  }
  .btn_page {
    width: 200px;
  }
}

.logo_text {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.div_autho {
  display: flex;
  flex-direction: row;
  gap: 10px;
  height: 40px;
  justify-content: center;
  align-items: center;
  color: var(--bg-color);
  border-radius: 20px;
  background-color: var(--main-color);
}

.btn_page {
  transition: all 0.2s;
  font-weight: bold;
  text-decoration: none;
}

.btn_page:hover {
  opacity: 50%;
}

.active_page {
  color: var(--main-color);
  position: relative;
}

.active_page::after {
  content: "";
  position: absolute;
  left: -10%;
  bottom: -2px;
  width: 120%;
  height: 2px;
  background-color: var(--main-color);
}
.img {
  height: 30px;
  aspect-ratio: 1/1;
}
.dropbtn {
  background-color: var(--main-color);
  color: white;
  border-radius: 5%;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  border: none;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  left: -60px;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: flex;
  flex-direction: column;
}

.dropdown:hover .dropbtn {
  background-color: #f45b5b;
}
</style>
