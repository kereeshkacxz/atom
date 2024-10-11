<template>
  <div
    style="
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 30px;
    "
  >
    <h1>Testing</h1>
    <FileInput @filesSelected="handleFilesSelected" />
    <div
      class="scrollmenu"
      @wheel="handleScroll"
      ref="scrollMenu"
    >
    <a
        v-for="(file, index) in extractedFiles"
        :key="index"
        @click="selectItem(index)"
        :class="{ active: selectedIndex === index }"
      >
        {{ file.name }}
      </a>
    </div>
    <h2>Содержимое выбранного файла:</h2>
    <div v-if="selectedFileContent" class="file-content">
      <pre>{{ selectedFileContent }}</pre>
    </div>
  </div>
</template>

<script setup>
import mammoth from 'mammoth'; 

const extractedFiles = ref([]);
const scrollMenu = ref(null);
const selectedIndex = ref(0);
const selectedFileContent = ref(null);

const handleFilesSelected = (files) => {
  extractedFiles.value = files.map((file) => {
    const match = file.name.match(/Use Case CF_(.+?)(\.[^.]+)?$/);
    return file;
  });
  if (files.length > 0) {
    loadFileContent(files[0]);
  }
};

const handleScroll = (event) => {
  event.preventDefault(); 
  scrollMenu.value.scrollLeft += event.deltaY; 
};

const selectItem = (index) => {
  selectedIndex.value = index; 
  loadFileContent(extractedFiles.value[index]);
};

const loadFileContent = (file) => {
  const reader = new FileReader();
  reader.onload = (event) => {
    const arrayBuffer = event.target.result; 
    mammoth.extractRawText({ arrayBuffer: arrayBuffer })
      .then((result) => {
        const text = result.value;
        // Используем nextTick, чтобы дождаться обновления DOM
        nextTick(() => {
          const wrappedText = wrapLongLines(text);
          selectedFileContent.value = wrappedText; 
        });
      })
      .catch((err) => {
        console.error("Ошибка при извлечении текста:", err);
      });
  };
  reader.readAsArrayBuffer(file); 
};

const wrapLongLines = (text) => {
  const tempElement = document.createElement('div');
  tempElement.style.visibility = 'hidden';
  tempElement.style.position = 'absolute';
  tempElement.style.whiteSpace = 'nowrap';
  document.body.appendChild(tempElement);

  const container = document.querySelector('.file-content');
  
  // Проверяем, существует ли контейнер
  if (!container) {
    console.error("Контейнер .file-content не найден.");
    document.body.removeChild(tempElement); // Удаляем временный элемент
    return text; // Возвращаем оригинальный текст, если контейнер не найден
  }

  const containerWidth = container.clientWidth; // Ширина контейнера
  const words = text.split(' ');
  let wrappedText = '';
  let currentLine = '';

  words.forEach((word) => {
    tempElement.innerText = currentLine + word; // Устанавливаем текст для измерения
    const textWidth = tempElement.clientWidth; // Получаем ширину текста

    if (textWidth > containerWidth) {
      wrappedText += currentLine.trim() + '\n'; // Добавляем текущую строку с переносом
      currentLine = word + ' '; // Начинаем новую строку с текущего слова
    } else {
      currentLine += word + ' '; // Добавляем слово в текущую строку
    }
  });

  wrappedText += currentLine.trim(); // Добавляем оставшуюся часть текста
  document.body.removeChild(tempElement); // Удаляем временный элемент
  return wrappedText;
};



</script>

<style scoped>
button {
  width: 200px;
}

.scrollmenu {
  width: 80vw;
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

.file-content {
  width: 80vw; 
  max-width: 100%; 
  background-color: #1e1e1e; 
  color: #ffffff; 
  overflow: hidden; /* Изменено с hidden на auto для прокрутки */
  padding: 10px; 
  border: 1px solid #ccc; 
  border-radius: 5px; 
  text-align: left;
}
.file-content pre {
  width: 80vw;
  overflow-wrap: break-word; /* Переносит длинные слова */
}
</style>
