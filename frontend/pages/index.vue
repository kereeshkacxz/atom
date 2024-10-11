<template>
  <div style="display: flex; flex-direction: column">
    <h1>Testing</h1>
    <h1>{{ tmp }}</h1>
  </div>
</template>
<script setup>
const { $api } = useNuxtApp();
const tmp = ref("");
async function fetchData() {
  // try {
  //   const response = await $api.get(`api/v1/health_check/ping`);
  //   tmp.value = response.data;
  // } catch (error) {
  //   console.error(error);
  // }
}
onMounted(() => {
  fetchData();
});
</script>
<style scoped></style>
