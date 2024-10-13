<template></template>

<script setup>
const router = useRouter();

onMounted(() => {
  router.push({ name: "testing" });
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
