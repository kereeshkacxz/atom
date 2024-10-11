<template>
  <ChipBox v-model="selectedChips" :availableChips="availableChipsList" />
</template>

<script setup>
const selectedChips = ref([]);
const availableChipsList = ref([
  "Chip 1",
  "Chip 2",
  "Chip 3",
  "Chip 4",
  "Chip 5",
]);
</script>

<style scoped></style>
