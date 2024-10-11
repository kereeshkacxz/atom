<template>
  <div class="person-information">
    <h1>Личный кабинет</h1>

    <div>
      <h3>Логин</h3>
      <CInput
        class="text"
        placeholder="Введите логин"
        v-model="username"
        :readonly="true"
      />
    </div>

    <div>
      <h3>Email</h3>
      <CInput
        class="input"
        placeholder="Введите email"
        v-model="information.email"
        :readonly="true"
      />
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const information = ref({});
const username = ref("");

async function fetchData() {
  try {
    const responseInformation = await $api.get(`api/v1/user/me`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    information.value = responseInformation.data;
    username.value = information.value.username;
  } catch (error) {
    console.error("Ошибка загрузки данных", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

onMounted(() => {
  fetchData();
  fetch();
});

let createNotification;

function fetch() {
  createNotification = inject("createNotification");
}
</script>

<style scoped>
.person-information {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar {
  line-height: 0;
  display: inline-block;
  margin: 5px;
  border: 4px solid rgba(200, 200, 200, 0.4);
  border-radius: 50%;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.4);
  transition: linear 0.25s;
  height: 128px;
  width: 128px;
}
.img {
  aspect-ratio: 1/1;
  height: 30px;
}
.edit-button {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  bottom: 10px;
  right: 10px;
  background-color: var(--main-color);
  opacity: 80%;
  aspect-ratio: 1/1;
  width: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-button:hover {
  background-color: rgba(0, 0, 0, 0.5);
}

.div_btn {
  margin-top: 20px;
}

.btn {
  width: 200px;
  height: 40px;
}
</style>
