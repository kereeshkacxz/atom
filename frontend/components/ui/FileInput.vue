<template>
  <CButton :class="{ inactive: !active }" @click="triggerFileInput">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      class="file_input_input"
      accept="*"
    />
    <span class="file_input_label">{{ label }}</span>
  </CButton>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    default: "Выберите файл",
  },
  active: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["fileSelected"]);

const fileInput = ref(null);

const triggerFileInput = () => {
  if (props.active) {
    fileInput.value.click();
  }
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    emit("fileSelected", file);
  }
};
</script>

<style scoped>
.file_input_input {
  display: none;
}

.file_input_label {
  pointer-events: none;
}
</style>
