<template>
  <div class="wrapper_swapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <div class="text-area-content">
      <div class="left-wrapper">
        <textarea v-model="textContent" @input="handleTextChange">Some text...</textarea>
      </div>
      <CButton class="btn" @click="analytics"
        >Get analytics</CButton
      >
      <div class="right-wrapper">
        <textarea readonly></textarea>
      </div>
    </div>
    <div class="wrapper">
      <ChipBox
        v-model="selectedChips"
        :availableChips="availableChips"
      />
    </div>
  </div>
</template>

<script setup>

import { parserName } from "~/utils/parserName.js";

const { $api } = useNuxtApp();
const curTab = ref(1);
const router = useRouter();
const availableChips = ref(["one"]);
const selectedChips = ref([]);
const textContent = ref('Some text...');
let debounceTimeout = null;

async function fetchData() {
  try {
    const responseFolders = await $api.get(`api/v1/folders`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    availableChips.value = responseFolders.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}
function changeTab() {
  router.push({ name: "testing" });
}

async function analytics() {};

function handleTextChange() {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout);
  }

  debounceTimeout = setTimeout(() => {
    const names = parserName("", textContent.value, availableChips.value);
    selectedChips.value = names;
    console.log(names);
  }, 1000); 
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
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
.wrapper_swapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
}
.text-area-content {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 40px;
  justify-content: space-between;
}

.text-area-content button {
  height: 70px;
  width: 250px;
}

textarea {
  width: 100%;
  height: 300px;
  padding: 12px 20px;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  background-color: var(--editor-color);
  font-size: 16px;
  resize: none;
}
.left-wrapper{
  width: 50%;
}
.right-wrapper{
  width: 50%;
}

@media (max-width: 768px) {
  .text-area-content {
    flex-direction: column; /* Изменяем направление на column */
    align-items: center;
  }
  .left-wrapper, .right-wrapper {
    width: 100%; /* Устанавливаем ширину на 100% для мобильных устройств */
  }
}
</style>
