<template>
  <div class="wrapper_swapper">
    <AtomHeader :index="curTab" @changeIndex="changeTab" />
    <div class="wrapper">
      <FileInput @filesSelected="handleFilesSelected" class="file_uploader" />

      <div class="slider" v-if="extractedFiles.length > 0">
        <button class="arrow left-arrow" @click="scrollLeft">&#9664;</button>

        <div class="scrollmenu" @wheel="handleScroll" ref="scrollMenu">
          <a
            v-for="(file, index) in extractedFiles"
            :key="index"
            @click="selectItem(index)"
            :class="{ active: selectedIndex === index }"
          >
            {{ file.name }}
          </a>
        </div>

        <button class="arrow right-arrow" @click="scrollRight">&#9654;</button>
      </div>

      <ChipBox
        v-if="selectedIndex !== null"
        v-model="selectedChips[selectedIndex]"
        :availableChips="availableChips"
      />
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp();
const curTab = ref(0);
const route = useRoute();
const router = useRouter();

function changeTab(newValue) {
  router.push({ name: "creating" });
}
const extractedFiles = ref([]);
const scrollMenu = ref(null);
const selectedIndex = ref(null);
const selectedChips = ref([]);
const availableChips = ref(["tmp", "tmp2"]);

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
    console.error("Ошибка получения данных:", error);
    createNotification(`${error.response.data.detail}`, "error");
  }
}

const handleFilesSelected = (files) => {
  extractedFiles.value = files.map((file) => {
    const match = file.name.match(/Use Case CF_(.+?)(\.[^.]+)?$/);
    return file;
  });
  selectedIndex.value = 0;
  selectedChips.value = new Array(extractedFiles.value.length).fill([]);
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
  if (from.fullPath === route.fullPath && extractedFiles.value.length > 0) {
    if (
      confirm(
        "Вы уверены, что хотите покинуть страницу? Внесенные изменения не сохранятся."
      )
    ) {
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

.arrow:hover {
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
</style>
