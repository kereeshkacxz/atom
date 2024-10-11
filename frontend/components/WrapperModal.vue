<template>
  <div class="bg_modal" @click="handleClickOutside">
    <div class="content_modal" @click.stop>
      <button class="close_button" @click="closeModal">✕</button>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from "vue";

const emit = defineEmits(["closeModal"]);

const handleClickOutside = () => {
  emit("closeModal");
};

const closeModal = () => {
  emit("closeModal");
};

const disableScroll = () => {
  document.body.style.overflow = "hidden";
};

const enableScroll = () => {
  document.body.style.overflow = "";
};

onMounted(() => {
  disableScroll();
});

onBeforeUnmount(() => {
  enableScroll();
});
</script>

<style scoped>
.bg_modal {
  position: fixed;
  left: 0;
  top: 0;
  background: var(--bg-modal-grad);
  width: 100vw;
  height: 100vh;
  z-index: 3;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content_modal {
  position: relative;
  min-width: 100px;
  min-height: 100px;
  background: var(--bg-grad);
  padding: 50px 30px;
  border-radius: 10px;
}

.close_button {
  position: absolute;
  top: 10px;
  right: 20px;
  background: transparent;
  border: none;
  user-select: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: 800;
}
.close_button:hover {
  color: var(--main-color);
}
</style>
