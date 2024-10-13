<template>
  <div class="report-display">
    <div class="file-name">{{ report.fileName }}</div>
    <div class="report-status">{{ report.status }}</div>
    <div class="report-description">{{ report.description }}</div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  report: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.report-display {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: var(--editor-color);
}

.report-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 3px;
  background-color: #fff;
}

.report-status {
  font-weight: bold;
}

.report-description {
  margin-top: 5px;
}

.no-reports {
  color: #777;
  text-align: center;
}
.file-name {
  color: var(--main-color);
}
</style>
