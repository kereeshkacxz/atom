<template>
  <div class="toggle_switch" @click="handleToggle">
    <div
      class="toggle_button"
      :class="{ toggle_buttonOn: isOn, toggle_buttonOff: !isOn }"
    >
      {{ isOn ? "Да" : "Нет" }}
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Boolean, required: true },
});
const emit = defineEmits(["update:modelValue"]);
const isOn = ref(props.modelValue);

function handleToggle() {
  isOn.value = !isOn.value;
  emit("update:modelValue", isOn.value);
}

watch(
  () => props.modelValue,
  (newValue) => {
    isOn.value = newValue;
  }
);
</script>

<style scoped>
.toggle_switch {
  --w: 30px;

  width: calc(var(--w) * 2 - 3px);
  height: var(--w);
  background-color: var(--editor-color);
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;

  user-select: none;
}
.toggle_button {
  border-radius: 5px;
  position: absolute;
  width: var(--w);
  height: var(--w);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: bold;

  transition: transform 0.3s ease, background-color 0.3s ease, color 0.3s ease;
  color: #fff;
}

.toggle_buttonOn {
  transform: translateX(var(--w));
  background-color: var(--success-color);
  box-shadow: 0px 0px 16px -2px var(--success-color);
}

.toggle_buttonOff {
  transform: translateX(0);
  background-color: var(--unsuccess-color);
  box-shadow: 0px 0px 16px -2px var(--unsuccess-color);
}
</style>
