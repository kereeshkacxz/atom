<template>
  <div class="wrapper_panel">
    <div class="block">
      <h2>Add New Certifiable Object:</h2>
      <CInput class="input" placeholder="Enter object name" v-model="name" />
      <CButton @click="addFolder">Add Object</CButton>
    </div>
    <div class="block">
      <h2>Add Regulation Files:</h2>
      <SelectableList
        :items="foldersName"
        :curIdx="currentFolder"
        @changeIndex="(i) => (currentFolder = i)"
      />
      <FileInput @filesSelected="handleFilesSelected" class="file_uploader" />

      <div class="added-files">
        <h3>Added Files:</h3>
        <div
          v-for="(file, index) in extractedFiles"
          :key="index"
          class="added-file"
        >
          <NuxtImg
            preload
            class="icon delete-icon"
            src="/cross.png"
            @click.stop="removeFile(index)"
          />
          {{ file.name }}
        </div>
      </div>

      <CButton @click="addFiles">Add Regulations</CButton>
    </div>
    <div class="block" v-if="isSuperAdmin">
      <h2>Add New Admin:</h2>
      <CInput class="input" placeholder="Enter username" v-model="login" />
      <CInput
        class="input"
        placeholder="Enter password"
        v-model="password"
        type="password"
      />
      <CInput class="input" placeholder="Enter email" v-model="email" />
      <CButton @click="addAdmin">Add Admin</CButton>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  isSuperAdmin: Boolean,
  extractedFiles: Array,
  folders: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits([
  "addFolder",
  "addFiles",
  "addAdmin",
  "handleFilesSelected",
]);

const name = ref("");
const login = ref("");
const email = ref("");
const password = ref("");
const currentFolder = ref(-1);

const foldersName = computed(() => {
  return props.folders.map((folder) => folder.name);
});

const removeFile = (index) => {
  props.extractedFiles.splice(index, 1);
};

const addFolder = () => {
  emit("addFolder", name.value);
  name.value = "";
};

const addFiles = () => {
  emit("addFiles", currentFolder.value);
  currentFolder.value = -1;
};

const addAdmin = () => {
  emit("addAdmin", {
    username: login.value,
    password: password.value,
    email: email.value,
  });
  login.value = "";
  password.value = "";
  email.value = "";
};

const handleFilesSelected = (files) => {
  emit("handleFilesSelected", files);
};
</script>

<style>
.wrapper_panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 40px;
}
.block {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  width: 500px;
}
.input {
  width: 100%;
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
