<template>
  <div class="wrapper_swapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <div class="wrapper">
      <FileInput @filesSelected="handleFilesSelected" class="file_uploader" />

      <div class="slider" v-if="extractedFiles.length > 0">
        <button
          class="arrow left-arrow"
          @click="scrollLeft"
          :class="{
            disabled: isLeftArrowDisabled,
          }"
        >
          &#9664;
        </button>

        <div class="scrollmenu" @wheel="handleScroll" ref="scrollMenu">
          <a
            v-for="(fileObject, index) in extractedFiles"
            :key="index"
            @click="selectItem(index)"
            :class="{
              error: errorChips.includes(index),
              active: selectedIndex === index && !errorChips.includes(index),
            }"
          >
            {{ fileObject.file.name }}
          </a>
        </div>

        <button
          class="arrow right-arrow"
          @click="scrollRight"
          :class="{
            disabled: isRightArrowDisabled,
          }"
        >
          &#9654;
        </button>
      </div>

      <ChipBox
        v-if="selectedIndex !== null"
        v-model="selectedChips[selectedIndex]"
        :availableChips="availableChips"
        :removable="visiblerReport.length === 0"
      />
      <CButton
        class="btnGenerate"
        v-if="extractedFiles.length > 0 && visiblerReport.length === 0"
        @click="validation"
        :active="!isLoading"
      >
        Generate Report
      </CButton>
      <div
        class="report-displays"
        v-if="visiblerReport.length > 0 && extractedFiles.length > 0"
      >
        <h2 style="color: var(--success-color)">
          Correct files: {{ correctFilesCount }}
        </h2>
        <h2 style="color: var(--unsuccess-color)">
          Incorrect files: {{ incorrectFilesCount }}
        </h2>
        <ReportDisplay :report="visiblerReport[selectedIndex]" />
        <CButton
          class="btnDownload"
          @click="downloadReport"
          :active="!isLoading"
        >
          Download Report
        </CButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import mammoth from "mammoth";
import { jsPDF } from "jspdf";
const { $api } = useNuxtApp();
const curTab = ref(0);
const router = useRouter();
import { parserName } from "~/utils/parserName.js";

function changeTab(newValue) {
  router.push({ name: "creating" });
}

const extractedFiles = ref([]);
const scrollMenu = ref(null);
const selectedIndex = ref(null);
const selectedChips = ref([]);
const availableChips = ref([]);
const errorChips = ref([]);
const visiblerReport = ref([]);
const correctFilesCount = ref(0);
const incorrectFilesCount = ref(0);
const isLoading = ref(false);
const jsonToPDF = ref({});
const isLeftArrowDisabled = computed(
  () => selectedIndex.value === 0 || extractedFiles.value.length === 0
);
const isRightArrowDisabled = computed(
  () =>
    selectedIndex.value === extractedFiles.value.length - 1 ||
    extractedFiles.value.length === 0
);

async function downloadReport() {
  if (isLoading.value) return;
  isLoading.value = true;
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("Verification Results", 10, 10);

  doc.setFontSize(12);
  const marginLeft = 10; // Left margin
  const lineHeight = 10; // Line height for spacing

  let currentY = 20; // Starting Y position for statistics

  // Add statistics at the beginning
  const positiveText = `Positive: ${jsonToPDF.value.statistics.positive}`;
  const negativeText = `Negative: ${jsonToPDF.value.statistics.negative}`;

  const positiveLines = doc.splitTextToSize(positiveText, 190);
  const negativeLines = doc.splitTextToSize(negativeText, 190);

  positiveLines.forEach((line) => {
    doc.text(line, marginLeft, currentY);
    currentY += lineHeight; // Move down for the next line
  });

  negativeLines.forEach((line) => {
    doc.text(line, marginLeft, currentY);
    currentY += lineHeight; // Move down for the next line
  });

  // Add some space before the answers
  currentY += 10; // Add extra space before answers

  // Add answers
  jsonToPDF.value.list_answers.forEach((answer, index) => {
    const answerText = `${extractedFiles.value[index].file.name}: ${answer.result}`; // Updated line
    const descriptionText = `Description: ${answer.description}`;

    // Split text to fit within the PDF width
    const answerLines = doc.splitTextToSize(answerText, 190); // 190 is the width
    const descriptionLines = doc.splitTextToSize(descriptionText, 190);

    // Add answer lines to PDF
    answerLines.forEach((line) => {
      doc.text(line, marginLeft, currentY);
      currentY += lineHeight; // Move down for the next line
    });

    // Add description lines to PDF
    descriptionLines.forEach((line) => {
      doc.text(line, marginLeft, currentY);
      currentY += lineHeight; // Move down for the next line
    });

    // Add some space between answers
    currentY += 5; // Add extra space after each answer
  });

  doc.save("results.pdf");
  isLoading.value = false;
}

async function fetchData() {
  try {
    const responseFolders = await $api.get(`api/v1/folders`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    availableChips.value = responseFolders.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}
function validation() {
  errorChips.value = [];
  selectedChips.value.map((selected, index) => {
    if (selected.length <= 0) errorChips.value.push(index);
  });
  if (errorChips.value.length > 0) {
    createNotification("Regulations are not selected for all files!", "error");
    return;
  }
  testing();
}

async function testing() {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    const responseFolders = await $api.post(
      `api/v1/gpt/analyze_list`,
      {
        simples: extractedFiles.value.map((fileObject, index) => {
          return {
            text: fileObject.content,
            folders_ids: selectedChips.value[index].map((chip) => {
              return chip.id;
            }),
          };
        }),
      },
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    visiblerReport.value = [];

    responseFolders.data.list_answers.forEach((report, index) => {
      visiblerReport.value.push({
        status: report.result,
        description: report.description,
        fileName: extractedFiles.value[index].file.name,
      });
    });
    correctFilesCount.value = responseFolders.data.statistics.positive;
    incorrectFilesCount.value = responseFolders.data.statistics.negative;
    createNotification(
      "All files have been checked, and reports have been generated.",
      "success"
    );
    jsonToPDF.value = responseFolders.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
  isLoading.value = false;
}

const handleFilesSelected = (files) => {
  extractedFiles.value = [];
  selectedChips.value = [];
  visiblerReport.value = [];
  selectedIndex.value = null;
  const fileReadPromises = files.map((file) => {
    if (file.type === "text/plain") {
      return loadTextFileContent(file)
        .then((content) => {
          if (content.length > 0) {
            extractedFiles.value.push({ file: file, content: content });
            selectedChips.value.push([]); // Инициализируем пустой массив для выбранных чипов
            const names = parserName(file.name, content, availableChips.value);
            selectedChips.value[selectedChips.value.length - 1] = names; // Сохраняем имена
          }
        })
        .catch((error) => {
          createNotification(`Ошибка чтения файла: ${file.name}`, "error");
        });
    } else {
      return loadFileContent(file)
        .then((content) => {
          if (content.length > 0) {
            extractedFiles.value.push({ file: file, content: content });
            selectedChips.value.push([]); // Инициализируем пустой массив для выбранных чипов
            const names = parserName(file.name, content, availableChips.value);
            selectedChips.value[selectedChips.value.length - 1] = names; // Сохраняем имена
          }
        })
        .catch((error) => {
          createNotification(`Ошибка чтения файла: ${file.name}`, "error");
        });
    }
  });

  Promise.all(fileReadPromises).then(() => {
    if (extractedFiles.value.length > 0) {
      selectedIndex.value = 0; // Устанавливаем индекс выбранного элемента, если есть файлы
    } else {
      selectedIndex.value = null; // Сбрасываем индекс, если нет файлов
    }
  });
};

const loadTextFileContent = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      resolve(text);
    };
    reader.onerror = (err) => {
      reject(err);
    };
    reader.readAsText(file);
  });
};

const loadFileContent = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const arrayBuffer = event.target.result;
      mammoth
        .extractRawText({ arrayBuffer: arrayBuffer })
        .then((result) => {
          const text = result.value;
          resolve(text); // Возвращаем содержимое файла
        })
        .catch((err) => {
          console.error("Ошибка при извлечении текста:", err);
          reject(err); // Отклоняем промис в случае ошибки
        });
    };
    reader.onerror = (err) => {
      reject(err); // Отклоняем промис в случае ошибки чтения файла
    };
    reader.readAsArrayBuffer(file);
  });
};

const handleScroll = (event) => {
  event.preventDefault();
  scrollMenu.value.scrollLeft += event.deltaY;
};

const scrollLeft = () => {
  const itemWidth = scrollMenu.value.children[selectedIndex.value].offsetWidth;
  scrollMenu.value.scrollLeft -= itemWidth;
  changeIndex(-1);
};

const scrollRight = () => {
  const itemWidth = scrollMenu.value.children[selectedIndex.value].offsetWidth;
  scrollMenu.value.scrollLeft += itemWidth;
  changeIndex(1);
};

const changeIndex = (direction) => {
  if (selectedIndex.value === null) {
    selectedIndex.value = 0;
  } else {
    const newIndex = selectedIndex.value + direction;
    if (newIndex >= 0 && newIndex < extractedFiles.value.length) {
      selectItem(newIndex);
    }
  }
};

const selectItem = (index) => {
  selectedIndex.value = index;
};

const handleKeydown = (event) => {
  if (event.key === "ArrowLeft") {
    scrollLeft();
  } else if (event.key === "ArrowRight") {
    scrollRight();
  }
};

router.beforeEach((to, from, next) => {
  if (extractedFiles.value.length > 0) {
    const confirmLeave = confirm(
      "Are you sure you want to leave this page? Unsaved changes will be lost."
    );
    if (confirmLeave) {
      extractedFiles.value = [];
      next();
    } else {
      next(false);
    }
  } else {
    next();
  }
});

onMounted(() => {
  fetchData();
  fetch();
  window.addEventListener("keydown", handleKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKeydown);
});

let createNotification;

function fetch() {
  createNotification = inject("createNotification");
}
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
.file_uploader {
  width: 200px;
}

.slider {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.scrollmenu {
  overflow-x: auto;
  background-color: #333;
  white-space: nowrap;
  user-select: none;
}

div.scrollmenu a {
  display: inline-block;
  color: white;
  text-align: center;
  border: 2px solid black;
  padding: 14px;
  text-decoration: none;
  transition: background-color 0.3s;
  cursor: pointer;
}

div.scrollmenu a:hover {
  background-color: #777;
}

div.scrollmenu a.active {
  background-color: var(--main-color30);
  color: #ffffff;
}

.arrow {
  background: none;
  border: none;
  color: var(--main-color70);
  font-size: 2em;
  cursor: pointer;
  padding: 0 10px;
}

.arrow:hover,
.arrow:active {
  color: #777;
}

.file-content {
  width: 80vw;
  max-width: 100%;
  background-color: #1e1e1e;
  color: #ffffff;
  overflow: hidden;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: left;
}

.file-content pre {
  width: 80vw;
  overflow-wrap: break-word;
}
.wrapper_swapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
}
.btn {
  width: 300px;
  height: 60px;
  font-size: 20px;
}
.error {
  background-color: var(--unsuccess-color);
  color: #ffffff;
}
.disabled {
  color: #777;
  cursor: default;
}
.btnDownload,
.btnGenerate {
  margin-top: 25px;
  padding: 10px 10px;
  font-size: 1.2em;
  width: 250px;
}
</style>
