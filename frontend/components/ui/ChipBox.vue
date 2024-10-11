<template>
  <div class="wrapper">
    <div class="problems_add">
      <SelectableList
        :items="availableChips"
        :curIdx="currentChip"
        @changeIndex="(i) => (currentChip = i)"
      />
      <CButton @click="addChip">Добавить</CButton>
    </div>
    <div class="chip-container">
      <div class="chip" v-for="(chip, index) in chips" :key="index">
        <span>{{ chip }}</span>
        <img
          preload
          src="~/public/cross.png"
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

const emit = defineEmits(); // Определяем emit

const currentChip = ref(-1);

// Инициализируем chips значением из modelValue
const chips = ref([...props.modelValue]);

const removeChip = (index) => {
  chips.value.splice(index, 1);
  emit("update:modelValue", chips.value); // Обновляем v-model
};

const addChip = () => {
  if (currentChip.value >= 0) {
    const chipToAdd = props.availableChips[currentChip.value];
    if (chipToAdd) {
      chips.value.push(chipToAdd);
      emit("update:modelValue", chips.value); // Обновляем v-model
      currentChip.value = -1; // Сброс текущего индекса после добавления
    }
  }
};

// Вычисляемый массив доступных чипов
const availableChips = computed(() => {
  return props.availableChips.filter((chip) => !chips.value.includes(chip));
});

// Синхронизация chips с modelValue при изменении
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
}

.problems_add {
  display: flex;
  gap: 20px;
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
