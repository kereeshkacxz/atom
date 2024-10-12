<template>
  <WrapperModal v-if="isOpenModal" @closeModal="close">
    <div v-if="type === 1" class="block">
      <h2>Смена логина на {{ username }}</h2>
      <p style="color: var(--main-color70)">Для подтверждения введите пароль</p>
      <h3>Пароль</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Введите пароль"
        v-model="oldPassword"
      />
      <CButton @click="saveChanges">Сохранить изменения</CButton>
    </div>
    <div class="block" v-else>
      <h2>Смена пароля:</h2>
      <p style="color: var(--main-color70)">
        Для подтверждения введите старый пароль
      </p>
      <h3>Старый пароль</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Введите старый пароль"
        v-model="oldPassword"
      />
      <h3>Новый пароль</h3>
      <CInput
        class="input"
        type="password"
        placeholder="Введите новый пароль"
        v-model="newPassword"
      />
      <CButton @click="saveChanges">Сохранить изменения</CButton>
    </div>
  </WrapperModal>

  <div class="person-information">
    <h1>Личный кабинет</h1>

    <div class="block">
      <h3>Email</h3>
      <CInput
        class="input"
        placeholder="Введите email"
        v-model="information.email"
        :readonly="true"
      />
    </div>
    <div class="block">
      <h3>Логин</h3>
      <CInput class="input" placeholder="Введите логин" v-model="username" />
    </div>
    <CButton @click="open(1)">Сохранить изменения</CButton>
    <CButton @click="open(2)">Изменить пароль</CButton>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue";
import { useNuxtApp } from "#app";

const { $api } = useNuxtApp();
const information = ref({});
const username = ref("");
const oldPassword = ref("");
const newPassword = ref("");

const isOpenModal = ref(false);
const type = ref(0);

function open(newValue) {
  type.value = newValue;
  isOpenModal.value = true;
}

function close() {
  isOpenModal.value = false;
  // Clear passwords when closing the modal
  oldPassword.value = "";
  newPassword.value = "";
}

async function saveChanges() {
  try {
    const endpoint =
      type.value === 1
        ? `api/v1/user/me_update?username=${username.value}&old_password=${oldPassword.value}`
        : `api/v1/user/me_update?old_password=${oldPassword.value}&password=${newPassword.value}`;

    const responseInformation = await $api.put(
      endpoint,
      {},
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    createNotification(`Изменения успешно сохранены!`, "success");
    close(); // Close the modal after saving changes
  } catch (error) {
    console.error("Ошибка загрузки данных", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

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

.block {
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input {
  width: 250px;
}
</style>
