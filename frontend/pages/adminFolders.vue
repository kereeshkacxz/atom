<template>
  <div class="wrapper_folders">
    <div v-for="folder in folders" :key="folder.id" class="folder">
      <div class="title" @click="toggleFolder(folder.id)">
        <div v-if="isOpen(folder.id)" class="icons">
          <NuxtImg
            preload
            class="icon"
            src="http://localhost:3000/_nuxt/public/minus.png"
          />
          <NuxtImg
            preload
            class="icon"
            src="http://localhost:3000/_nuxt/public/open_folder.png"
          />
        </div>
        <div v-else class="icons">
          <NuxtImg
            preload
            class="icon"
            src="http://localhost:3000/_nuxt/public/plus.png"
          />
          <NuxtImg
            preload
            class="icon"
            src="http://localhost:3000/_nuxt/public/folder.png"
          />
        </div>
        {{ folder.name }}
        <NuxtImg
          preload
          class="icon delete-icon"
          src="http://localhost:3000/_nuxt/public/cross.png"
          @click.stop="confirmRemoveFolder(folder)"
        />
      </div>
      <div class="files" v-if="isOpen(folder.id)">
        <div v-for="file in folder.files" :key="file.id" class="file">
          <NuxtImg
            preload
            class="icon"
            src="http://localhost:3000/_nuxt/public/file.png"
          />
          {{ file.name }}
          <NuxtImg
            preload
            class="icon delete-icon"
            src="http://localhost:3000/_nuxt/public/cross.png"
            @click.stop="confirmDeleteFile(file, folder.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  folders: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["removeFolder", "deleteFile", "fetchFiles"]);

const openFolders = ref(new Set());

const isOpen = (folderId) => {
  return openFolders.value.has(folderId);
};

const toggleFolder = async (folderId) => {
  if (openFolders.value.has(folderId)) {
    openFolders.value.delete(folderId);
  } else {
    openFolders.value.add(folderId);
    emit("fetchFiles", folderId);
  }
};

const confirmRemoveFolder = (folder) => {
  emit("open", 1, folder.name, { folder: folder });
};

const confirmDeleteFile = (file, folderId) => {
  emit("open", 2, file.name, { file: file, id: folderId });
};
</script>

<style>
.folder {
  text-align: left;
  user-select: none;
  margin: 5px 0;
}
.files {
  margin-left: 40px;
}
.file {
  gap: 5px;
  display: flex;
  justify-content: start;
  align-items: center;
  margin: 4px 0;
}
.title {
  cursor: pointer;
  gap: 5px;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
}
.wrapper_folders {
  width: 100%;
  display: flex;
  flex-direction: column;
}
.icon {
  aspect-ratio: 1/1;
  height: 20px;
}
.icons {
  display: flex;
  align-items: center;
  justify-content: center;
}
.delete-icon {
  cursor: pointer;
  transition: all 0.2s;
}
.delete-icon:hover {
  opacity: 70%;
  transform: scale(140%);
}
</style>
