<template>
  <l-map
    :zoom="initialZoom"
    :center="center"
    style="height: 100vh; width: 100vw;"
    :useGlobalLeaflet="false"
  >
    <l-tile-layer
      :url="tileUrl"
      :options="tileOptions"
      name="A Big Image Service"
    />
  </l-map>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      center: [0, 0], // Центр карты (координаты можно настроить)
      initialZoom: -20, // Начальный уровень зума
      tileUrl: "http://127.0.0.1:8000/microscope/{z}/tiles/{x}_{y}.png", // URL для загрузки тайлов
      tileOptions: {
        maxZoom: 6, // Максимальный уровень зума
        minZoom: -20, // Минимальный уровень зума
        tileSize: 512, // Размер тайла
        noWrap: false, // Запретить бесконечное прокручивание
      },
    };
  },
};
</script>
