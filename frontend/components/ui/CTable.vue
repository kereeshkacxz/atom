<template>
  <table class="custom_table">
    <thead>
      <tr>
        <th
          v-for="(header, index) in headers"
          :key="index"
          :class="{ to_left: to_left.includes(index + 1) }"
          @click="handleHeaderClick(index)"
        >
          <slot :name="'header' + (index + 1)">
            {{ header }}
          </slot>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(row, rowIndex) in rows"
        :key="rowIndex"
        @click="handleRowClick(row)"
        class="table_row"
        :class="{ odd_row: rowIndex % 2 == 0, canClickRow: canClickRow }"
      >
        <td
          v-for="(column, colIndex) in row"
          :key="colIndex"
          :class="{ to_left: to_left.includes(colIndex + 1) }"
          :style="{
            width: columnWidths[colIndex] ? columnWidths[colIndex] : 'auto',
          }"
        >
          <slot
            :name="'column' + (colIndex + 1)"
            :row="row"
            :rowIndex="rowIndex"
          >
            {{ column }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>

const props = defineProps({
  headers: {
    type: Array,
    required: true,
  },
  rows: {
    type: Array,
    required: true,
  },
  to_left: {
    type: Array,
    required: true,
  },
  columnWidths: {
    type: Array,
    default: () => [],
  },
  canClickRow: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["rowClick", "headerClick"]);

function handleRowClick(row) {
  emit("rowClick", row);
}
function handleHeaderClick(index) {
  emit("headerClick", index);
}
</script>

<style scoped>
.custom_table {
  width: 100%;
  border-spacing: 4px;
}

.custom_table th {
  position: sticky;
  top: 0;
  background-color: var(--editor-color);
  opacity: 100%;
  z-index: 1;
}

.header {
  text-align: left;
  width: 100%;
}

.odd_row {
  background-color: var(--second-color);
}

th {
  cursor: pointer;
  user-select: none;
}

.custom_table th,
.custom_table td {
  padding: 12px;
}

.to_left {
  text-align: left;
  align-items: left;
}

.table_row {
  transition: background-color 0.1s ease, transform 0.1s ease;
}

.canClickRow:hover {
  cursor: pointer;
  background-color: var(--main-color);
  transform: scale(1.02);
}
</style>
