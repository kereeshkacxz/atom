<template>
  <div class="wrapper_swapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <div class="wrapper"></div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const curTab = ref(1);
const router = useRouter();

async function fetchData() {}
function changeTab() {
  router.push({ name: "testing" });
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
</style>
