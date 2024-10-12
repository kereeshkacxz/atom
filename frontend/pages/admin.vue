<template>
  <WrapperModal v-if="isOpenModal" @closeModal="close">
    <h2>
      Вы уверены, что хотите удалить {{ type === 1 ? "объект" : "регламент" }}
    </h2>
    <h2>с названием {{ title }}?</h2>
    <CButton style="margin-top: 20px" @click="condirmDelete">Удалить!</CButton>
  </WrapperModal>
  <div class="wrapper" v-if="isAdmin">
    <div class="wrapper_fodler">
      <div v-for="folder in folders" :key="folder.id" class="folder">
        <div class="title" @click="toggleFolder(folder.id)">
          <div v-if="isOpen(folder.id)" class="icons">
            <NuxtImg
              preload
              class="icon"
              src="http://localhost:3000/_nuxt/public/minus.png"
            />
            <NuxtImg
              preload
              class="icon"
              src="http://localhost:3000/_nuxt/public/open_folder.png"
            />
          </div>
          <div v-else class="icons">
            <NuxtImg
              preload
              class="icon"
              src="http://localhost:3000/_nuxt/public/plus.png"
            />
            <NuxtImg
              preload
              class="icon"
              src="http://localhost:3000/_nuxt/public/folder.png"
            />
          </div>
          {{ folder.name }}
          <NuxtImg
            preload
            class="icon delete-icon"
            src="http://localhost:3000/_nuxt/public/cross.png"
            @click.stop="open(1, folder.name, { folder: folder })"
          />
        </div>
        <div class="files" v-if="isOpen(folder.id)">
          <div v-for="file in folder.files" :key="file.id" class="file">
            <NuxtImg
              preload
              class="icon"
              src="http://localhost:3000/_nuxt/public/file.png"
            />
            {{ file.name }}
            <NuxtImg
              preload
              class="icon delete-icon"
              src="http://localhost:3000/_nuxt/public/cross.png"
              @click.stop="open(2, file.name, { file: file, id: folder.id })"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="wrapper_panel">
      <div class="block">
        <h2>Добавить новый сертифицируемый объект:</h2>
        <CInput
          class="input"
          placeholder="Введите название объекта"
          v-model="name"
        />
        <CButton @click="addFolder">Добавить объект</CButton>
      </div>
      <div class="block">
        <h2>Добавить файлы регламента:</h2>
        <SelectableList
          :items="foldersName"
          :curIdx="currentFolder"
          @changeIndex="(i) => (currentFolder = i)"
        />
        <FileInput @filesSelected="handleFilesSelected" class="file_uploader" />

        <div class="added-files">
          <h3>Добавленные файлы:</h3>
          <div
            v-for="(file, index) in extractedFiles"
            :key="index"
            class="added-file"
          >
            <NuxtImg
              preload
              class="icon delete-icon"
              src="http://localhost:3000/_nuxt/public/cross.png"
              @click.stop="removeFile(index)"
            />
            {{ file.name }}
          </div>
        </div>

        <CButton @click="addFiles">Добавить регламенты</CButton>
      </div>
      <div class="block" v-if="isSuperAdmin">
        <h2>Добавить нового админа:</h2>
        <CInput class="input" placeholder="Введите логин" v-model="login" />
        <CInput
          class="input"
          placeholder="Введите пароль"
          v-model="password"
          type="password"
        />
        <CInput class="input" placeholder="Введите почту" v-model="email" />
        <CButton @click="addAdmin">Добавить админа</CButton>
      </div>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const isAdmin =
  localStorage.getItem("admin") === "true" ||
  localStorage.getItem("superadmin") === "true";
const isSuperAdmin = localStorage.getItem("superadmin") === "true";

const extractedFiles = ref([]);
const folders = ref([]);
const name = ref("");
const login = ref("");
const email = ref("");
const password = ref("");

const title = ref("");
const type = ref("");
const openFolders = ref(new Set());
const currentFolder = ref(-1);
const paramsFunc = ref({});

const isOpenModal = ref(false);

function condirmDelete() {
  isOpenModal.value = false;
  if (type.value === 1) {
    removeFolder(paramsFunc.value.folder);
  } else {
    deleteFile(paramsFunc.value.file, paramsFunc.value.id);
  }
}

function close() {
  isOpenModal.value = false;
  confirmed.value = false;
  type.value = "";
  title.value = "";
}
function open(typeNew, titleNew, params) {
  type.value = typeNew;
  title.value = titleNew;
  isOpenModal.value = true;
  paramsFunc.value = params;
}
const toggleFolder = (folderId) => {
  if (openFolders.value.has(folderId)) {
    openFolders.value.delete(folderId);
  } else {
    openFolders.value.add(folderId);
    fetchFiles(folderId);
  }
};

const isOpen = (folderId) => {
  return openFolders.value.has(folderId);
};

const removeFile = (index) => {
  extractedFiles.value.splice(index, 1);
};

async function removeFolder(folder) {
  try {
    // Удаляем папку на сервере
    await $api.delete(`api/v1/folders/${folder.id}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    // Удаляем папку из локального состояния
    folders.value = folders.value.filter(
      (newFolder) => newFolder.id !== folder.id
    );

    createNotification("Объект успешно удален", "success");
  } catch (error) {
    console.error("Ошибка удаления объекта:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addFiles() {
  if (currentFolder.value === -1) {
    createNotification(`Выберите сертифицируемый объект`, "error");
    return;
  }
  if (extractedFiles.value.length === 0) {
    createNotification(`Выберите файлы`, "error");
    return;
  }

  try {
    const folderId = folders.value[currentFolder.value].id; // Получаем ID текущей папки

    for (const file of extractedFiles.value) {
      const formData = new FormData();
      formData.append("file", file); // Добавляем файл в FormData

      await $api.post(`api/v1/files/?folder_id=${folderId}`, formData, {
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data", // Указываем, что отправляем FormData
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
    }

    await fetchFiles(folderId);

    if (!isOpen(folderId)) {
      toggleFolder(folderId);
    }

    name.value = "";
    createNotification("Файлы успешно добавлены", "success");
  } catch (error) {
    console.error("Ошибка добавления файлов:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addFolder() {
  if (name.value === "") {
    createNotification(`Наименование объекта не может быть пустым.`, "error");
    return;
  }
  try {
    const response = await $api.post(
      `api/v1/folders/?folder_name=${name.value}`,
      {},
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    folders.value.push({
      id: response.data.id,
      name: name.value,
      files: [],
    });

    name.value = "";

    createNotification("Папка успешно добавлена", "success");
  } catch (error) {
    console.error("Ошибка создания объекта:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function fetchFiles(id) {
  try {
    const responseFiles = await $api.get(`api/v1/files/?folder_id=${id}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });

    const folder = folders.value.find((folder) => folder.id === id);
    if (!folder.files) {
      folder.files = [];
    }
    folder.files = responseFiles.data;
  } catch (error) {
    console.error("Ошибка получения данных:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function deleteFile(file, folderId) {
  try {
    await $api.delete(`api/v1/files/${file.id}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    const folder = folders.value.find((folder) => folder.id === folderId);
    folder.files = folder.files.filter((fileNew) => fileNew.id !== file.id);

    createNotification("Файл успешно удален", "success");
  } catch (error) {
    console.error("Ошибка удаления файла:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function fetchData() {
  try {
    const responseFolders = await $api.get(`api/v1/folders`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    folders.value = responseFolders.data;
  } catch (error) {
    console.error("Ошибка получения данных:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addAdmin() {
  try {
    const response = await $api.post(
      `api/v1/user/register/admin`,
      {
        username: login.value,
        password: password.value,
        email: email.value,
        type: "admin",
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    createNotification("Успешно зарегистрированы!", "success");
  } catch (error) {
    console.error("Ошибка регистрации:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

const handleFilesSelected = (files) => {
  extractedFiles.value = files.map((file) => {
    return file;
  });
};

const foldersName = computed(() => {
  return folders.value.map((folder) => folder.name);
});
onMounted(() => {
  fetchData();
  fetch();
});

let createNotification;

function fetch() {
  createNotification = inject("createNotification");
}
</script>

<style>
.folder {
  text-align: left;
  user-select: none;
  margin: 5px 0;
}
.files {
  margin-left: 40px;
}
.file {
  gap: 5px;
  display: flex;
  justify-content: start;
  align-items: center;
  margin: 4px 0;
}
.title {
  cursor: pointer;

  gap: 5px;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
}
.wrapper {
  gap: 40px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
@media (max-width: 768px) {
  /* Замените 768px на желаемую ширину для мобильных устройств */
  .wrapper {
    flex-direction: column; /* Изменяем на column для мобильных устройств */
  }
}
.icon {
  aspect-ratio: 1/1;
  height: 20px;
}
.icons {
  display: flex;
  align-items: center;
  justify-content: center;
}
.delete-icon {
  cursor: pointer;
  transition: all 0.2s;
}
.delete-icon:hover {
  opacity: 70%;
  transform: scale(140%);
}
.input {
  width: 100%;
}
.block {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.wrapper_panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
}
h2 {
  color: var(--main-color70);
}
.added-files {
  margin-top: 10px;
}
.added-file {
  text-align: start;
  max-width: 500px;
  gap: 10px;
  display: flex;
  justify-content: start;
  align-items: center;
  margin: 5px 0;
}
</style>
