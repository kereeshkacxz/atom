<template>
  <div class="button_header">
    <CButton
      class="btn"
      :class="{ active: index === 0 }"
      @click="setItemIndex(0)"
      >Проверить требование</CButton
    >
    <CButton
      class="btn"
      :class="{ active: index === 1 }"
      @click="setItemIndex(1)"
      >Создать требование</CButton
    >
  </div>
</template>

<script setup>
const emit = defineEmits(["changeIndex"]);

const props = defineProps({
  index: { type: Number, required: true },
});

const localCurItem = ref(props.index);

function setItemIndex(index) {
  localCurItem.value = index;
  emit("changeIndex", localCurItem.value);
}

watch(
  () => props.index,
  (newIndex) => {
    localCurItem.value = newIndex;
  }
);
</script>

<style scoped>
.button_header {
  width: 100%;
  gap: 40px;
  display: flex;
  height: 60px;
}
.btn {
  border-radius: 10px;
  flex: 1;
}
.active {
  border: 1px solid var(--main-color);
  pointer-events: none;
}
</style>
