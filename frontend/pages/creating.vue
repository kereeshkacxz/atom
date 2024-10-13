<template>
  <div class="wrapper_swapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <div class="text-area-content">
      <div class="left-wrapper">
        <textarea
          v-model="textContent"
          @input="handleTextChange"
          placeholder="Write your requirements..."
        ></textarea>
      </div>
      <div class="wrapper_buttons_ii">
        <CButton
          class="btnAnalyze"
          @click="analyze"
          :active="!isLoading"
          :class="[{ disabled: isLoading }]"
          >{{ isLoading ? "Loading..." : "Analyze" }}</CButton
        >
        <CButton
          class="btnNormalyze"
          @click="normalize"
          :active="!isLoading"
          :class="[{ disabled: isLoading }]"
          >{{ isLoading ? "Loading..." : "Normalize" }}</CButton
        >
      </div>

      <div class="right-wrapper">
        <textarea readonly v-model="answer"></textarea>
      </div>
    </div>
    <div class="wrapper">
      <ChipBox
        v-model="selectedChips"
        :availableChips="availableChips"
        @deleteChip="deleteChip"
      />
      <div class="card-container">
        <ChipContent
          v-for="chip in chipsToVisible"
          :key="chip.id"
          :id="chip.id"
          :name="chip.name"
          :content="chip.content"
        />
      </div>
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
const deletedChips = ref([]);
const chipsToVisible = ref([]);
const textContent = ref("");
const answer = ref("");
const isLoading = ref(false);
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

async function analyze() {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    const responseFolders = await $api.post(
      `api/v1/gpt/analyze`,
      {
        text: textContent.value.replace('"', "'"),
        folders_ids: selectedChips.value.map((chip) => {
          return chip.id;
        }),
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    answer.value =
      "Result - " +
      responseFolders.data.result +
      "\n" +
      responseFolders.data.description;
    createNotification(`Text successful analyzed.`, "success");
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`Unable to analyze the text.`, "error");
  }
  isLoading.value = false;
}
async function normalize() {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    const responseFolders = await $api.post(
      `api/v1/gpt/normalize/?text=${textContent.value}`,
      {},
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    createNotification(`Text successful normalized.`, "success");
    textContent = responseFolders.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`Unable to display the text in the template`, "error");
  }
  isLoading.value = false;
}

async function short_requirements() {
  chipsToVisible.value = chipsToVisible.value.filter((chip) =>
    selectedChips.value.some((selectedChip) => selectedChip.id === chip.id)
  );

  const allSelectedChipsVisible = selectedChips.value.every((selectedChip) =>
    chipsToVisible.value.some((chip) => chip.id === selectedChip.id)
  );

  if (allSelectedChipsVisible) {
    return;
  }

  const missingChipIds = selectedChips.value
    .filter(
      (selectedChip) =>
        !chipsToVisible.value.some((chip) => chip.id === selectedChip.id)
    )
    .map((selectedChip) => selectedChip.id);

  try {
    const response = await $api.post(
      `api/v1/gpt/shortly`,
      {
        folders_ids: missingChipIds,
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    const newChips = response.data;

    for (const [key, value] of Object.entries(newChips)) {
      if (!chipsToVisible.value.some((visibleChip) => visibleChip.id === key)) {
        chipsToVisible.value.push({
          id: key,
          name: value[0], // Используем первый элемент массива как имя
          content: value[1], // Используем второй элемент массива как контент
        });
      }
    }
  } catch (error) {
    console.error("Error fetching new chips:", error);
    createNotification(`Unable to load shortly requirements`, "error");
  }
}

function handleTextChange() {
  if (textContent.value == "") deletedChips.value = [];
  if (debounceTimeout) {
    clearTimeout(debounceTimeout);
  }

  debounceTimeout = setTimeout(() => {
    const names = parserName("", textContent.value, availableChips.value);
    names.forEach((name) => {
      if (
        !selectedChips.value.includes(name) &&
        !deletedChips.value.includes(name)
      ) {
        selectedChips.value.push(name);
      }
    });
    selectedChips.value = [...selectedChips.value];
  }, 1000);
}

function deleteChip(chip) {
  if (!deletedChips.value.includes(chip)) deletedChips.value.push(chip);
}

watch(selectedChips, (newValue, oldValue) => {
  short_requirements();
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

.btnAnalyze,
.btnNormalyze {
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
textarea:focus {
  outline: none !important;
  border: 1px solid var(--main-color);
  box-shadow: 0 0 10px var(--main-color30);
}
.left-wrapper {
  width: 50%;
}
.right-wrapper {
  width: 50%;
}
.wrapper_buttons_ii {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
@media (max-width: 768px) {
  .text-area-content {
    flex-direction: column; /* Изменяем направление на column */
    align-items: center;
  }
  .left-wrapper,
  .right-wrapper {
    width: 100%; /* Устанавливаем ширину на 100% для мобильных устройств */
  }
  .wrapper_buttons_ii {
    flex-direction: row;
    gap: 10px;
    width: 100%;
  }
  .btnAnalyze,
  .btnNormalyze {
    width: 100%;
  }
  .text-area-content {
    gap: 20px;
  }
}
.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
.disabled {
  cursor: wait;
  opacity: 70%;
}
</style>
