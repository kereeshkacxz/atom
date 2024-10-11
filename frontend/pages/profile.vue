<template>
  <div class="person-information">
    <h1>Личный кабинет</h1>

    <div>
      <div class="avatar-container" @mouseover="showEditButton = true" @mouseleave="showEditButton = false">
        <NuxtImg
          preload
          :src="avatarSrc"
          class="avatar"
        />
        <div class="edit-button" @click="triggerFileInput">
          <img class="img" src="~/public/edit.png" />
        </div>
      </div>
      <h3>Логин</h3>
      <CInput
        class="text"
        placeholder="Введите логин"
        v-model="username"
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

    <div>
      <h3>Дата рождения</h3>
      <CInputDate
        class="input"
        placeholder="Выберите дату рождения"
        v-model="born"
      />
    </div>
    
    <div class="div_btn">
      <CButton class="btn" @click="saveChange">
        Сохранить
      </CButton>
    </div>

    <input type="file" accept="image/*" ref="fileInput" @change="handleFileChange" style="display: none;" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue';

const { $api } = useNuxtApp();
const information = ref({});
const username = ref("");
const born = ref("");
const showEditButton = ref(false);
const selectedFile = ref(null);
const fileInput = ref(null); 

const avatarSrc = computed(() => {
  return `http://localhost:8080/api/v1/images/id/${information.value.avatar_id}`;
});

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
    born.value = information.value.born;
  } catch (error) {
    console.error("Ошибка загрузки данных", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function saveChange() {
  try {
    const response = await $api.put(
      `api/v1/user/me_update?username=${username.value}`,
      {},
      {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    createNotification("Изменения внесены!", "success");
  } catch (error) {
    console.error("Ошибка сохранения:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

function handleFileChange(event) {
  selectedFile.value = event.target.files[0];
  if (selectedFile.value) {
    uploadAvatar();
  }
}

async function uploadAvatar() {
  if (!selectedFile.value) {
    createNotification("Пожалуйста, выберите файл", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await $api.post(`api/v1/user/setAvatar`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    createNotification("Аватар успешно загружен!", "success");
    information.value.avatar_id = response.data.avatar_id; 
  } catch (error) {
    console.error("Ошибка загрузки аватара:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

function triggerFileInput() {
  if (fileInput.value) {
    fileInput.value.click();
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
