<template>
  <l-map
    ref="map"
    :zoom="initialZoom"
    :center="center"
    style="height: 100vh; width: 100vw;"
    :useGlobalLeaflet="false"
    :max-bounds="bounds"
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
      initialZoom: 0, // Начальный уровень зума
      tileUrl: "http://127.0.0.1:8000/microscope/{z}/tiles/{x}_{y}.png", // URL для загрузки тайлов
      bounds: [
        [-10000, -10000], // Нижний левый угол
        [10000, 10000],   // Верхний правый угол
      ],
      tileOptions: {
        maxZoom: 6, // Максимальный уровень зума
        minZoom: 0, // Минимальный уровень зума
        tileSize: 64, // Размер тайла
        noWrap: true, // Запретить бесконечное прокручивание
        errorTileUrl: 'http://http.cat/404',
      },
    };
  }
};
</script>
