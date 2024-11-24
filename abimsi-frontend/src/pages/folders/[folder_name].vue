<script setup>
</script>

<template>
  <v-row>
    <v-col
      v-for="n in 1"
      :key="n"
      class="d-flex child-flex"
      cols="4"
    >
      <v-card max-width="500" max-height="500" min-width="200" min-height="200">
        <v-img
          lazy-src="https://mirea.dsvinka.ru/api/info/bio_cut/preview.png"
          src="https://mirea.dsvinka.ru/api/info/bio_cut/preview.png"
          aspect-ratio="1"
          class="bg-grey-lighten-2"
          cover
        >
          <template v-slot:placeholder>
            <v-row
              align="center"
              class="fill-height ma-0"
              justify="center"
            >
              <v-progress-circular
                color="grey-lighten-5"
                indeterminate
              ></v-progress-circular>
            </v-row>
          </template>
        </v-img>

        <v-card-actions>
          <v-card-text>Срез живой ткани</v-card-text>

          <v-btn to="/views/bio_cut">Перейти</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="sass">

</style>
