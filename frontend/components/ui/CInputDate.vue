<template>
  <CInput
    :placeholder="placeholder"
    type="datetime-local"
    :modelValue="formattedModelValue"
    @update:modelValue="updateValue"
    @focus="$emit('focus', $event)"
    @blur="$emit('blur', $event)"
    @input="handleInput"
  />
</template>

<script setup>
import { formatDateForInput } from "~/utils/formatDate.js";
import CInput from "./CInput.vue";
const props = defineProps({
  placeholder: { default: "", type: String },
  modelValue: { default: "", type: [String, Number] },
});

const emit = defineEmits(["update:modelValue", "focus", "input", "blur"]);

const formattedModelValue = computed(() => {
  if (props.modelValue) {
    return props.modelValue.includes("Z")
      ? formatDateForInput(props.modelValue)
      : props.modelValue;
  }
  return "";
});

function updateValue(value) {
  emit("update:modelValue", value);
}

function handleInput(event) {
  const value = event.target.value;
  updateValue(value);
}
</script>
