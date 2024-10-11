<template>
  <div class="wrapper">
    <div class="problems_add">
      <SelectableList
        :items="availableChipsNamed"
        :curIdx="currentChip"
        @changeIndex="(i) => (currentChip = i)"
      />
      <CButton @click="addChip">Добавить</CButton>
    </div>
    <div class="chip-container">
      <div class="chip" v-for="(chip, index) in chips" :key="chip.id">
        <span>{{ chip.name }}</span>
        <NuxtImg
          preload
          src="http://localhost:3000/_nuxt/public/cross.png"
          @click="removeChip(index)"
          class="remove-button"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, watch, defineEmits } from "vue";

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
  },
  availableChips: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits();
const currentChip = ref(-1);

const chips = ref([...props.modelValue]);

const removeChip = (index) => {
  chips.value.splice(index, 1);
  emit("update:modelValue", chips.value);
};

const addChip = () => {
  if (currentChip.value >= 0) {
    const chipToAdd = availableChips.value[currentChip.value];
    if (chipToAdd && !chips.value.some((chip) => chip.id === chipToAdd.id)) {
      chips.value.push(chipToAdd);
      emit("update:modelValue", chips.value);
    }
  }
};

const availableChips = computed(() => {
  return props.availableChips.filter(
    (chip) => !chips.value.some((existingChip) => existingChip.id === chip.id)
  );
});
const availableChipsNamed = computed(() => {
  return props.availableChips
    .filter(
      (chip) => !chips.value.some((existingChip) => existingChip.id === chip.id)
    )
    .map((chip) => chip.name);
});
watch(
  () => props.modelValue,
  (newValue) => {
    chips.value = [...newValue];
  }
);
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
}

.chip-container {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  flex-wrap: wrap;
  width: 100%;
  min-height: 70px;
}

.problems_add {
  display: flex;
  gap: 20px;
  width: 100%;
}

.chip {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  background-color: var(--main-color70);
  border-radius: 5px;
  margin: 5px;
}

.chip span {
  font-weight: 550;
  user-select: none;
}

.remove-button {
  color: var(--red-color);
  background: none;
  font-weight: 900;
  border: none;
  cursor: pointer;
  margin-left: 8px;
  font-size: 20px;
}

.remove-button:hover {
  color: black;
  transform: scale(1.1);
}

img {
  aspect-ratio: 1/1;
  height: 30px;
}
</style>
