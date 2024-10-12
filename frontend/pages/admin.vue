<template>
  <div class="admin_wrapper" v-if="isAdmin">
    <div class="folders">
      <AdminFolders :folders="folders" @open="open" @fetchFiles="fetchFiles" />
    </div>
    <div class="panel">
      <AdminPanel
        v-if="isAdmin"
        :folders="folders"
        :isSuperAdmin="isSuperAdmin"
        @addFolder="addFolder"
        @addFiles="addFiles"
        @addAdmin="addAdmin"
        :extractedFiles="extractedFiles"
        @handleFilesSelected="handleFilesSelected"
      />
    </div>

    <WrapperModal v-if="isOpenModal" @closeModal="close">
      <div v-if="type !== 3">
        <h2>
          Are you sure you want to delete
          {{ type === 1 ? "the object" : "the regulation" }}
          with the name
        </h2>
        <h2>
          <span style="color: white">"</span>
          <span style="color: var(--main-color70)">{{ title }}</span>
          <span style="color: white">" ?</span>
        </h2>
        <CButton style="margin-top: 20px" @click="confirmDelete"
          >Delete!</CButton
        >
      </div>
      <div v-if="type === 3">
        <h2>
          <span style="color: white">Are you sure you want to refresh </span>
          <span style="color: var(--main-color70)">the model</span>
          <span style="color: white">?</span>
        </h2>
        <CButton style="margin-top: 20px" @click="confirmDelete"
          >Refresh!</CButton
        >
      </div>
    </WrapperModal>
  </div>
</template>

<script setup>
import AdminFolders from "./adminFolders.vue";
import AdminPanel from "./adminPanel.vue";

const { $api } = useNuxtApp();

const isAdmin =
  localStorage.getItem("admin") === "true" ||
  localStorage.getItem("superadmin") === "true";

const isSuperAdmin = localStorage.getItem("superadmin") === "true";

const folders = ref([]);
const extractedFiles = ref([]);
const title = ref("");
const type = ref("");
const paramsFunc = ref({});
const isOpenModal = ref(false);

let createNotification;

function confirmDelete() {
  isOpenModal.value = false;
  if (type.value === 1) {
    removeFolder(paramsFunc.value.folder);
  } else if (type.value === 2) {
    deleteFile(paramsFunc.value.file, paramsFunc.value.id);
  } else {
    refreshModel();
  }
}

function close() {
  isOpenModal.value = false;
  type.value = "";
  title.value = "";
}

function open(typeNew, titleNew, params) {
  type.value = typeNew;
  title.value = titleNew;
  isOpenModal.value = true;
  paramsFunc.value = params;
}

async function removeFolder(folder) {
  try {
    await $api.delete(`/api/v1/folders/${folder.id}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    folders.value = folders.value.filter(
      (newFolder) => newFolder.id !== folder.id
    );
    createNotification("Object successfully deleted", "success");
  } catch (error) {
    console.error("Error deleting object:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function fetchFiles(folderId) {
  try {
    const response = await $api.get(`api/v1/files/?folder_id=${folderId}`);
    const folder = folders.value.find((f) => f.id === folderId);
    if (folder) {
      folder.files = response.data || [];
    }
  } catch (error) {
    console.error("Ошибка получения данных:", error);
    createNotification(error.response?.data?.detail || "Ошибка сети", "error");
  }
}

async function deleteFile(file, folderId) {
  try {
    await $api.delete(`/api/v1/files/${file.id}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    const folder = folders.value.find((folder) => folder.id === folderId);
    folder.files = folder.files.filter((fileNew) => fileNew.id !== file.id);
    createNotification("File successfully deleted", "success");
  } catch (error) {
    console.error("Error deleting file:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addFiles(currentFolder) {
  if (currentFolder === -1) {
    createNotification("Please select a certifiable object", "error");
    return;
  }
  if (extractedFiles.value.length === 0) {
    createNotification("Please select files", "error");
    return;
  }

  try {
    const folderId = folders.value[currentFolder].id;

    for (const file of extractedFiles.value) {
      const formData = new FormData();
      formData.append("file", file);

      await $api.post(`/api/v1/files/?folder_id=${folderId}`, formData, {
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
    }
    await fetchFiles(folderId);
    createNotification("Files successfully added", "success");
  } catch (error) {
    console.error("Error adding files:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addFolder(name) {
  if (name === "") {
    createNotification("The name of the object cannot be empty.", "error");
    return;
  }
  try {
    const response = await $api.post(
      `/api/v1/folders/?folder_name=${name}`,
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
      name: name,
      files: [],
    });

    createNotification("Folder successfully added", "success");
  } catch (error) {
    console.error("Error creating object:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

async function addAdmin(params) {
  if (!params.username) {
    createNotification("The username cannot be empty.", "error");
    return;
  }
  if (!params.password) {
    createNotification("The password cannot be empty.", "error");
    return;
  }
  if (!params.email) {
    createNotification("The email cannot be empty.", "error");
    return;
  }
  try {
    const response = await $api.post(
      `api/v1/user/register/admin`,
      {
        username: params.username,
        password: params.password,
        email: params.email,
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

async function fetchData() {
  try {
    const responseFolders = await $api.get(`/api/v1/folders`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    folders.value = responseFolders.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}
async function refreshModel() {
  createNotification(`The model has been successfully updated!`, "success");
}

function fetch() {
  createNotification = inject("createNotification");
}

const handleFilesSelected = (files) => {
  extractedFiles.value = files.map((file) => {
    return file;
  });
};

onMounted(() => {
  fetchData();
  fetch();
});
</script>

<style>
.admin_wrapper {
  display: flex;
  gap: 40px;
  width: 100%;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
.folders {
  width: 40%;
}
.panel {
  width: 60%;
}
.modal {
  color: var(--main--color);
}
@media (max-width: 768px) {
  .admin_wrapper {
    flex-direction: column;
  }
  .folders {
    width: 100%;
  }
  .panel {
    width: 100%;
  }
}
</style>
