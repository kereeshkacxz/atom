<template>
  <div class="menu_wrapper">
    <NuxtLink
      v-for="(item, index) in items"
      :key="index"
      :class="['menu_item fc', { underline: index === curItem }]"
      :to="item[1]"
    >
      {{ item[0] }}
    </NuxtLink>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  items: { default: [], type: Array, required: true },
  curItem: { default: 0, type: Number },
});

const route = useRoute();
const curItem = ref(0);

const updateCurItem = () => {
  curItem.value = props.items.findIndex((item) => {
    return (
      item[1].name === route.name ||
      (item.length > 2 && item[2].name === route.name)
    );
  });
};

watch(route, updateCurItem, { immediate: true });
</script>

<style scoped>
.menu_item {
  user-select: none;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 90%;
  text-decoration: none;
}
.menu_item:hover {
  opacity: 100%;
  color: var(--main-color);
}
.underline {
  position: relative;
}
.underline::after {
  content: "";
  position: absolute;
  left: -10%;
  bottom: -5px;
  width: 120%;
  height: 2px;
  background-color: var(--main-color);
}
.menu_wrapper {
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 50px;
  background-color: var(--second-color);
  width: 100%;
  height: 60px;
}
</style>
