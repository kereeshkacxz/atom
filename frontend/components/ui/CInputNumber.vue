<template>
  <CInput
    :placeholder="placeholder"
    :modelValue="modelValue"
    :unit="unit"
    @update:modelValue="updateValue"
    @focus="$emit('focus', $event)"
    @blur="$emit('blur', $event)"
    @input="handleInput"
  />
</template>

<script setup>
const props = defineProps({
  placeholder: { default: "", type: String },
  modelValue: { default: "", type: [String, Number] },
  unit: { type: String, default: "" },
});

const emit = defineEmits(["update:modelValue", "focus", "input", "blur"]);

function updateValue(value) {
  emit("update:modelValue", value);
}

function handleInput(event) {
  const value = event.target.value;
  const numericValue = value.replace(/[^0-9]/g, "");

  if (value !== numericValue) {
    event.target.value = numericValue;
  }

  updateValue(numericValue);
}
</script>
