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
        <CButton class="btnAnalyze" @click="analyze">Analyze</CButton>
        <CButton class="btnNormalyze" @click="normalize">Normalize</CButton>
      </div>

      <div class="right-wrapper">
        <textarea readonly></textarea>
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
const chipsToRequest = ref([]);
const chipsToVisible = ref([]);
const textContent = ref("");

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
  try {
    // const responseFolders = await $api.get(`api/v1/normalize`, {
    //   headers: {
    //     Accept: "application/json",
    //     "Content-Type": "application/json",
    //   },
    //   params: {
    //     text: textContent.value,
    //   },
    // });
    // availableChips.value = responseFolders.data;
    console.log({
      text: textContent.value,
      folders_id: selectedChips.value.map((chip) => {
        return chip.id;
      }),
    });
    createNotification(`Text successful analyzed.`, "success");
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`Unable to analyze the text.`, "error");
  }
}
async function normalize() {
  try {
    // const responseFolders = await $api.get(`api/v1/normalize`, {
    //   headers: {
    //     Accept: "application/json",
    //     "Content-Type": "application/json",
    //   },
    //   params: {
    //     text: textContent.value,
    //   },
    // });
    // availableChips.value = responseFolders.data;
    console.log({
      text: textContent.value,
    });
    createNotification(`Text successful normalized.`, "success");
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`Unable to display the text in the template`, "error");
  }
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
    // const response = await $api.get(`api/v1/short_requirement`, {
    //   headers: {
    //     Accept: "application/json",
    //     "Content-Type": "application/json",
    //   },
    //   params: {
    //     folders_id: missingChipIds,
    //   },
    // });
    console.log({ folders_id: missingChipIds });
    // const newChips = response.data;

    // newChips.forEach((chip) => {
    //   if (
    //     !chipsToVisible.value.some((visibleChip) => visibleChip.id === chip.id)
    //   ) {
    //     chipsToVisible.value.push(chip);
    //   }
    // });
    missingChipIds.map((chip) => {
      chipsToVisible.value.push({
        id: chip,
        name: "AVAS",
        content:
          "AVAS (Acoustic Vehicle Alerting System) — это система звукового оповещения для электромобилей и гибридов, которая издает искусственный шум на низких скоростях, чтобы предупреждать пешеходов о приближении транспортного средства.",
      });
    });
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
</style>
