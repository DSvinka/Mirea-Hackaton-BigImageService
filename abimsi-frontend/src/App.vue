<script setup>
import {Notifications} from "@kyvg/vue3-notification";

import {mdiDockLeft} from "@mdi/js";
import {ref} from "vue";
import Upload from "@/components/upload.vue";

const rail = ref(false)
</script>

<template>
  <v-app>
    <v-card>
      <v-layout>
        <div class="d-block position-fixed top-0">
          <v-btn class="ml-1" variant="flat" icon @click="rail = !rail">
            <v-icon class="text-grey-darken-2" :icon="mdiDockLeft"/>
          </v-btn>
        </div>

        <v-navigation-drawer permanent v-model="rail" class="ml-0 mt-13">
          <v-divider></v-divider>

          <v-list density="compact" nav>
            <v-list-item to="/folders/chleni" class="border-lg font-weight-bold" style="background-color: #e7c0ff"><span class="text-h7">Члены общества</span></v-list-item>
            <v-list-item to="/folders/ni-chleni"><span class="text-h7 font-weight-bold">Не члены общества</span></v-list-item>
            <v-list-item to="/folders/guinea-pigs"><span class="text-h7 font-weight-bold">Морские свинки</span></v-list-item>
            <v-list-item to="/folders/colony"><span class="text-h7 font-weight-bold">Колониум</span></v-list-item>
          </v-list>

          <v-btn class="d-block text-center d-flex mx-auto font-weight-bold" style="color: #bf7ecc" variant="flat">Создать папку</v-btn>

          <upload></upload>
        </v-navigation-drawer>

        <v-main style="min-height: 100vh" class="mt-13 mx-3">
          <router-view />
          <notifications position="bottom right" close-on-click :duration="3000"/>
        </v-main>
      </v-layout>
    </v-card>
  </v-app>
</template>
