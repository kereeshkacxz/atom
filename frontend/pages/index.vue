<template>
  <div class="wrapper" @click="focusInput">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <ChipBox v-model="selectedChips" :availableChips="availableChipsList" />
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const tmp = ref("");
const curTab = ref(0);

const selectedChips = ref([]);
const availableChipsList = ref([
  "Chip 1",
  "Chip 2",
  "Chip 3",
  "Chip 4",
  "Chip 5",
]);

function changeTab(newValue) {
  curTab.value = newValue;
}

async function fetchData() {
  try {
    const response = await $api.get(`api/v1/health_check/ping`);
    tmp.value = response.data;
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
}

.chip-container {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  flex-wrap: wrap;
}

.problems_add {
  display: flex;
  gap: 20px;
}

h2 {
  margin-top: 20px;
}
</style>
