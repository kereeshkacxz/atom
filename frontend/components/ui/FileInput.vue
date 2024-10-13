<template>
  <CButton :class="{ inactive: !active }" @click="triggerFileInput">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      class="file_input_input"
      accept="*"
      multiple
    />
    <span class="file_input_label">{{ label }}</span>
  </CButton>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    default: "Select Files",
  },
  active: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["filesSelected"]);

const fileInput = ref(null);

const triggerFileInput = () => {
  if (props.active) {
    fileInput.value.click();
  }
};

const handleFileChange = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    const fileArray = Array.from(files);
    emit("filesSelected", fileArray);
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
