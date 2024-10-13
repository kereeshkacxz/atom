<template>
  <div class="customCheckbox" @click="handleToggle">
    <div class="checkboxIndicator" :class="{ checked: isChecked }">
      <span v-if="isChecked">✔</span>
    </div>
    <span v-if="label" class="checkboxLabel">{{ label }}</span>
  </div>
</template>

<script setup>
const props = defineProps({
  value: { type: Boolean, required: true },
  label: { type: String, default: "" },
});

const emit = defineEmits(["changeValue"]);
const isChecked = ref(props.value);

function handleToggle() {
  isChecked.value = !isChecked.value;
  emit("changeValue", isChecked.value);
}

watch(
  () => props.value,
  (newValue) => {
    isChecked.value = newValue;
  }
);
</script>

<style scoped>
.customCheckbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkboxIndicator {
  width: 20px;
  height: 20px;
  border: 2px solid #ccc;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.checkboxIndicator.checked {
  background-color: #4caf50;
  border-color: #4caf50;
}

.checkboxLabel {
  margin-left: 8px;
  font-size: 18px;
}
</style>
