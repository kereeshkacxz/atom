<template>
  <div class="selectable-list" ref="dropdown" :key="componentKey">
    <div class="input-wrapper">
      <CInput
        type="text"
        v-model="searchQuery"
        :placeholder="currentLabel"
        @click="openDropdown"
      />
      <span class="arrow" :class="{ open: isOpen }">&#9662;</span>
    </div>
    <ul v-if="isOpen" class="dropdown">
      <li
        v-for="(item, index) in filteredItems || []"
        :key="index"
        @click="selectItem(index)"
        :class="{ selected: index === currentIndex }"
        class="option"
      >
        {{ item }}
      </li>
    </ul>
  </div>
</template>

<script setup>
const emits = defineEmits(["changeIndex"]);
const props = defineProps({
  items: { type: Array, default: () => [] },
  curIdx: { type: Number, default: -1 },
});

const searchQuery = ref("");
const currentIndex = ref(props.curIdx);
const isOpen = ref(false);
const filteredItems = ref([]);
const currentLabel = ref("Choose");
const dropdown = ref(null);
const componentKey = ref(0);

function openDropdown() {
  isOpen.value = true;
  searchQuery.value = "";
}

function closeDropdown() {
  isOpen.value = false;
  if (currentIndex.value >= 0 && currentIndex.value < props.items.length) {
    searchQuery.value = props.items[currentIndex.value];
  } else {
    searchQuery.value = "";
  }
}

function selectItem(index) {
  currentIndex.value = index;
  emits("changeIndex", index);
  closeDropdown();
}

function filterItems() {
  if (!Array.isArray(props.items)) {
    filteredItems.value = [];
    return;
  }

  filteredItems.value = props.items.filter((item) => {
    return (
      item !== undefined &&
      item !== null &&
      typeof item === "string" &&
      item.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
}

function handleClickOutside(event) {
  if (dropdown.value && !dropdown.value.contains(event.target)) {
    closeDropdown();
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  filterItems();
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

watch(searchQuery, () => {
  filterItems();
});

function updateSelectableContent() {
  componentKey.value += 1;
  filterItems();
}

watch(
  () => props.items,
  (newItems) => {
    updateSelectableContent();
  },
  { deep: true }
);
watch(
  () => props.curIdx,
  (newCurIdx) => {
    currentIndex.value = newCurIdx;
    if (newCurIdx >= 0 && newCurIdx < props.items.length) {
      searchQuery.value = props.items[newCurIdx];
    } else {
      searchQuery.value = "";
    }
  }
);
</script>

<style scoped>
.selectable-list {
  position: relative;
  width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.input-wrapper input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.arrow {
  position: absolute;
  right: 10px;
  pointer-events: none;
  transition: transform 0.3s ease;
}

.arrow.open {
  transform: rotate(180deg);
}

.dropdown {
  position: absolute;
  top: 100%;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  z-index: 1000;
  box-sizing: border-box;
}

.option {
  background-color: var(--editor-color);
  border-bottom: 1px solid var(--second-color);
  padding: 4px 20px;
  text-align: left;
  cursor: pointer;
  transition: padding 0.2s ease;
}

.option:hover {
  background-color: var(--main-color70);
  color: black;
  padding: 4px 10px;
}
</style>
