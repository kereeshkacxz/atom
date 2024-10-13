<template>
  <div class="card">
    <div class="card-header">
      <h3>{{ name }}</h3>
    </div>
    <div class="card-content">
      <p>{{ content }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    default: "",
  },
  content: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-header {
  font-size: 1.5em;
  margin-bottom: 8px;
}

.card-content {
  font-size: 1em;
  margin-bottom: 16px;
}

.card-footer {
  text-align: right;
}
</style>
