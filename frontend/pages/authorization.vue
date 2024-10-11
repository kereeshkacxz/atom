<template>
  <div class="wrapper_form">
    <div class="authorization" v-if="isExistAccount">
      <p class="label">Почта</p>
      <CInput
        class="input"
        placeholder="Введите почту"
        v-model="email"
        @keyup.enter="entryAccount"
      />
      <p class="label">Пароль</p>
      <CInput
        class="input"
        type="password"
        placeholder="Введите пароль"
        v-model="password"
        @keyup.enter="entryAccount"
      />
    </div>
    <div class="registration" v-else>
      <p class="label">Логин</p>
      <CInput
        class="input"
        placeholder="Введите логин"
        v-model="login"
        @keyup.enter="entryAccount"
      />
      <p class="label">Почта</p>
      <CInput
        class="input"
        placeholder="Введите почту"
        v-model="email"
        @keyup.enter="entryAccount"
      />
      <p class="label">Пароль</p>
      <CInput
        type="password"
        class="input"
        placeholder="Введите пароль"
        v-model="password"
        @keyup.enter="entryAccount"
      />
      <p class="label">Повтор пароля</p>

      <CInput
        type="password"
        class="input"
        placeholder="Повторите пароль"
        v-model="secondPassword"
        @keyup.enter="entryAccount"
      />
    </div>
    <div class="div_btn">
      <CButton class="btn" @click="entryAccount">
        {{ isExistAccount ? "Войти" : "Создать" }}</CButton
      >
      <p class="change_window" @click="changeWindow()">
        {{ isExistAccount ? "Создать аккаунт" : "Войти в аккаунт" }}
      </p>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const router = useRouter();

const login = ref("");
const email = ref("");
const password = ref("");
const secondPassword = ref("");

const isExistAccount = ref(true);
function changeWindow() {
  isExistAccount.value = !isExistAccount.value;
}

function entryAccount() {
  if (!isExistAccount.value && login.value === "") {
    createNotification("Введите логин", "error");
    return;
  }

  if (!isExistAccount.value && login.value.length < 5) {
    createNotification("Длина логина не менее 5 символов", "error");
    return;
  }

  if (password.value === "") {
    createNotification("Введите пароль", "error");
    return;
  }

  if (!isExistAccount.value && password.value !== secondPassword.value) {
    createNotification("Пароли не совпадают", "error");
    return;
  }

  if (!isExistAccount.value && password.value.length < 8) {
    createNotification("Длина пароля не менее 8 символов", "error");
    return;
  }

  if (email.value === "") {
    createNotification("Введите почту", "error");
    return;
  }

  if (!isExistAccount.value && !email.value.includes("@")) {
    createNotification("Неправильный формат почты!", "error");
    return;
  }

  if (!isExistAccount.value && email.value.length < 5) {
    createNotification("Длина почты не менее 5 символов", "error");
    return;
  }

  if (isExistAccount.value) {
    authorization();
  } else {
    registration();
  }
}

async function registration() {
  try {
    const response = await $api.post(
      `api/v1/user/register`,
      {
        username: login.value,
        password: password.value,
        email: email.value,
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    );
    createNotification("Успешно зарегистрированы!", "success");
    authorization();
  } catch (error) {
    console.error("Ошибка регистрации:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function authorization() {
  try {
    const response = await $api.post(
      `api/v1/user/auth`,
      {
        email: email.value,
        password: password.value,
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    );
    createNotification("Успешно авторизованы!", "success");
    localStorage.setItem("token", response.data.access_token);
    router.push("/").then(() => {
      location.reload();
    });
  } catch (error) {
    console.error("Ошибка авторизации:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

onMounted(() => {
  fetch();
  if (localStorage.getItem("token"))
    router.push("/").then(() => {
      location.reload();
    });
});
let createNotification;

function fetch() {
  createNotification = inject("createNotification");
}
</script>

<style scoped>
.wrapper_form {
  width: 500px;
  padding: 30px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
  background-color: var(--bg-color);
}

.input_div {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
  width: 100%;
}

.input {
  height: 40px;
  width: 300px;
  box-shadow: 0px 0px 8px -2px var(--main-color20);
}
.div_btn,
.btn {
  width: 100%;
}

.btn {
  height: 40px;
  margin-bottom: 10px;
}

.change_window {
  user-select: none;
  cursor: pointer;

  font-size: 15px;
  opacity: 70%;
}

.change_window:hover {
  opacity: 90%;
  color: var(--main-color);
}

.label {
  margin-top: 10px;
  opacity: 60%;
}
</style>
