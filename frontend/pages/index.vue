<template>
  <div class="wrapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <TestingSpecification v-if="curTab === 0" />
  </div>
</template>

<script setup>
import TestingSpecification from "./TestingSpecification.vue";
const { $api } = useNuxtApp();
const curTab = ref(0);

function changeTab(newValue) {
  curTab.value = newValue;
}

async function fetchData() {
  try {
    const response = await $api.get(`api/v1/health_check/ping`);
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

h2 {
  margin-top: 20px;
}
</style>
