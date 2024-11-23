<script setup>
import { ref, reactive, watch } from 'vue';
import axios from 'axios';

const CHUNK_SIZE = 1048576 * 100; // 100 MB

const showProgress = ref(false);
const progress = ref(0);
const fileState = reactive({
  fileSize: 0,
  fileId: '',
  totalChunks: 0,
  totalChunksUploaded: 0,
  startChunk: 0,
  endChunk: CHUNK_SIZE,
  fileToUpload: null,
  uploadedBytes: 0,
});

// Сброс состояния
const resetState = () => {
  Object.assign(fileState, {
    fileSize: 0,
    fileId: '',
    totalChunks: 0,
    totalChunksUploaded: 0,
    startChunk: 0,
    endChunk: CHUNK_SIZE,
    fileToUpload: null,
    uploadedBytes: 0,
  });
  progress.value = 0;
  showProgress.value = false;
};

// Запрос статуса файла и подготовка данных
const getFileContext = async (event) => {
  resetState();
  showProgress.value = true;
  const file = event.target.files[0];
  const fileId = `${file.size}-${file.lastModified}-${file.name}`;

  try {
    const { data } = await axios.get('http://localhost:3002/upload/status', {
      headers: {
        'x-file-name': fileId,
        'file-size': file.size,
      },
    });

    const uploadedBytes = data.uploaded || 0;
    const endingChunk = Math.min(uploadedBytes + CHUNK_SIZE, file.size);

    Object.assign(fileState, {
      fileSize: file.size,
      fileId,
      totalChunks: Math.ceil((file.size - uploadedBytes) / CHUNK_SIZE),
      totalChunksUploaded: 0,
      startChunk: uploadedBytes,
      endChunk:
        endingChunk === file.size ? endingChunk + 1 : endingChunk,
      fileToUpload: file,
      uploadedBytes,
    });

    if (fileState.fileSize > 0) {
      await fileUpload(fileState.totalChunksUploaded);
    }
  } catch (err) {
    console.error('Status call failed', err);
  }
};

// Отправка чанков
const uploadChunk = async (chunk) => {
  const { fileId, startChunk, endChunk, fileSize, totalChunksUploaded } =
    fileState;

  try {
    await axios.post('http://localhost:3002/upload/files', chunk, {
      headers: {
        'x-file-name': fileId,
        'Content-Range': `bytes ${startChunk}-${endChunk}/${fileSize}`,
        'file-size': fileSize,
      },
    });

    const endingChunk = Math.min(endChunk + CHUNK_SIZE, fileSize);

    Object.assign(fileState, {
      totalChunksUploaded: totalChunksUploaded + 1,
      startChunk: endChunk,
      endChunk: endingChunk === fileSize ? endingChunk + 1 : endingChunk,
      uploadedBytes: endingChunk,
    });

    const prog = fileSize ? (fileState.uploadedBytes / fileSize) * 100 : 0.1;
    progress.value = prog;
  } catch (err) {
    console.error('Chunk upload failed', err);
  }
};

// Процесс загрузки файла
const fileUpload = async (totalChunksUploaded) => {
  const { totalChunks, fileToUpload, startChunk, endChunk } = fileState;

  if (totalChunksUploaded <= totalChunks) {
    const chunk = fileToUpload.slice(startChunk, endChunk);
    await uploadChunk(chunk);
  } else {
    await axios.post('http://localhost:3002/upload/complete', null, {
      headers: {
        'x-file-name': fileState.fileId,
      },
    });
    resetState();
  }
};

watch(
  () => fileState.totalChunksUploaded,
  (newVal) => {
    if (newVal <= fileState.totalChunks) {
      fileUpload(newVal);
    }
  }
);
</script>

<template>
  <v-container>
    <v-file-input
      label="Выберите файл"
      @change="getFileContext"
      outlined
    />
    <v-progress-linear
      v-if="showProgress"
      :value="progress"
      height="20"
      color="blue"
      striped
      indeterminate
    >
      <strong>{{ progress.toFixed(2) }}%</strong>
    </v-progress-linear>
  </v-container>
</template>
