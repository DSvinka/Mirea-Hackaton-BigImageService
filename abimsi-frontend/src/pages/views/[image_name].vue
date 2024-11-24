<template>
  <div class="ml-10 mt-10">
    <div class="position-fixed right-0 bottom-0 mr-2 mb-2">
      <v-card class="px-2">
        <v-btn class="mx-1 my-1 bg-amber-lighten-4" variant="text" @click="zoomIn">Увеличить</v-btn>
        <v-btn class="mx-1 my-1 bg-amber-lighten-4" variant="text" @click="zoomOut">Уменьшить</v-btn>
        <v-btn class="mx-1 my-1 bg-red-lighten-4" variant="text" @click="resetView">Сбросить</v-btn>
        <span class="ml-3">Масштаб: {{ scaleText }}</span>
      </v-card>
    </div>

    <canvas
      class="w-auto h-auto"
      ref="canvas"
      @mousedown="startDrag"
      @mousemove="drag"
      @mouseup="stopDrag"
      @mouseleave="stopDrag"
      @wheel="handleWheel"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import {useRoute} from "vue-router";

const route = useRoute('/views/[image_name]')

const canvas = ref(null);
const ctx = ref(null);

const state = reactive({
  tileSize: 2048,
  buffer: 1,
  imageWidth: 0,
  imageHeight: 0,
  scale: 0.1,
  tileScale: 5,
  offsetX: 0,
  offsetY: 0,
  isDragging: false,
  startX: 0,
  startY: 0,
  tiles: {},
});

const scaleText = computed(() => `${(state.scale * 100).toFixed(2)} (${state.tileScale})`);

const init = async () => {
  const response = await fetch(`https://mirea.dsivnka.ru/api/info/${route.params.image_name}`);
  if (!response.ok) {
    throw new Error(`Response status: ${response.status}`);
  }

  const result = await response.json();
  state.imageWidth = result.size[0];
  state.imageHeight = result.size[1];

  canvas.value.width = window.innerWidth;
  canvas.value.height = window.innerHeight;

  ctx.value = canvas.value.getContext("2d");
  ctx.value.imageSmoothingEnabled = false;

  window.addEventListener("resize", resizeCanvas);
  renderTiles();
};

const resizeCanvas = () => {
  canvas.value.width = window.innerWidth;
  canvas.value.height = window.innerHeight;
  renderTiles();
};

const loadTile = (row, col) => {
  const tileKey = `${row}_${col}`;
  if (state.tiles[tileKey] && state.tiles[tileKey].scale === state.tileScale) {
    return state.tiles[tileKey];
  }

  const img = new Image();
  img.src = `https://mirea.dsivnka.ru/api/tiles/${route.params.image_name}/${state.tileScale}/${row * state.tileSize}_${col * state.tileSize}.png`;

  img.onload = () => {
    state.tiles[tileKey] = { img, scale: state.tileScale };
    renderTiles();
  };

  img.onerror = () => {
    console.error(`Ошибка загрузки изображения: ${img.src}`);
  };

  state.tiles[tileKey] = { img, scale: null };
  return state.tiles[tileKey];
};

const renderTiles = () => {
  const startCol = Math.floor((-state.offsetX - canvas.value.width * state.buffer) / (state.tileSize * state.scale));
  const endCol = Math.ceil((-state.offsetX + canvas.value.width * (1 + state.buffer)) / (state.tileSize * state.scale));
  const startRow = Math.floor((-state.offsetY - canvas.value.height * state.buffer) / (state.tileSize * state.scale));
  const endRow = Math.ceil((-state.offsetY + canvas.value.height * (1 + state.buffer)) / (state.tileSize * state.scale));

  for (let row = startRow; row <= endRow; row++) {
    for (let col = startCol; col <= endCol; col++) {
      if (
        row < 0 ||
        col < 0 ||
        row * state.tileSize >= state.imageWidth ||
        col * state.tileSize >= state.imageHeight
      )
        continue;

      const tileKey = `${row}_${col}`;
      const cachedTile = state.tiles[tileKey];
      const x = Math.round(state.offsetX + col * state.tileSize * state.scale);
      const y = Math.round(state.offsetY + row * state.tileSize * state.scale);
      const size = Math.round(state.tileSize * state.scale);

      if (cachedTile && cachedTile.img.complete) {
        ctx.value.drawImage(cachedTile.img, x, y, size, size);
      } else {
        const tile = loadTile(row, col);
        if (tile.img.complete) {
          ctx.value.drawImage(tile.img, x, y, size, size);
        }
      }
    }
  }
};

const zoom = (factor, mouseX, mouseY) => {
  const newScale = state.scale * factor;
  state.offsetX = mouseX - (mouseX - state.offsetX) * (newScale / state.scale);
  state.offsetY = mouseY - (mouseY - state.offsetY) * (newScale / state.scale);
  state.scale = newScale;

  const previousTileScale = state.tileScale;

  if (state.scale * 100 > 30) {
    state.tileScale = 0;
  } else if (state.scale * 100 > 20) {
    state.tileScale = 2;
  } else if (state.scale * 100 > 10) {
    state.tileScale = 4;
  } else {
    state.tileScale = 5;
  }

  if (state.tileScale !== previousTileScale) {
    state.tiles = {};
  }

  renderTiles();
};

const zoomIn = () => zoom(1.2, canvas.value.width / 2, canvas.value.height / 2);
const zoomOut = () => zoom(0.8, canvas.value.width / 2, canvas.value.height / 2);
const resetView = () => {
  state.offsetX = 0;
  state.offsetY = 0;
  state.scale = 1;
  renderTiles();
};

const startDrag = (event) => {
  state.isDragging = true;
  state.startX = event.clientX;
  state.startY = event.clientY;
};

const drag = (event) => {
  if (!state.isDragging) return;

  const dx = event.clientX - state.startX;
  const dy = event.clientY - state.startY;

  state.offsetX += dx;
  state.offsetY += dy;

  state.startX = event.clientX;
  state.startY = event.clientY;

  renderTiles();
};

const stopDrag = () => {
  state.isDragging = false;
};

const handleWheel = (event) => {
  event.preventDefault();
  const rect = canvas.value.getBoundingClientRect();
  const mouseX = event.clientX - rect.left;
  const mouseY = event.clientY - rect.top;
  const factor = event.deltaY < 0 ? 1.1 : 0.9;
  zoom(factor, mouseX, mouseY);
};

onMounted(init);
</script>

<style>
/* Стили остаются без изменений */
</style>
