<script setup>
import {Notifications} from "@kyvg/vue3-notification";

import {mdiDockLeft} from "@mdi/js";
import {ref} from "vue";
import Upload from "@/components/upload.vue";

const rail = ref(false)

import itelmaLogo from "@/assets/Itelma_Logos_Rus (Electronics).svg";
</script>

<template>
  <v-app>
    <v-card>
      <v-layout>
        <div class="d-block position-fixed top-0">
          <div class="d-flex">
            <v-btn class="ml-1" variant="flat" icon @click="rail = !rail">
              <v-icon class="text-grey-darken-2" :icon="mdiDockLeft"/>
            </v-btn>

            <v-card-title class="mx-auto">A Big Image Service</v-card-title>
          </div>

        </div>

        <v-navigation-drawer permanent v-model="rail" class="ml-0 mt-13 position-fixed left-0">
          <v-divider></v-divider>

          <v-list density="compact" nav>
            <v-list-item to="/folders/microscope" class="border-lg font-weight-bold" style="background-color: #e7c0ff"><span class="text-h7">Микроскоп</span></v-list-item>
          </v-list>

          <v-btn class="d-block text-center d-flex mx-auto font-weight-bold mt-5" disabled style="color: #bf7ecc" variant="text">Создать папку*</v-btn>

          <upload></upload>

          <template v-slot:append>
            <div class="pa-2 mb-2">
              <div class="text-body-2 text-center">
                Works on <span class="text-yellow-darken-3 font-weight-bold">ALT</span> <span class="font-weight-bold">Linux</span><br/>
                Supported by <span class="font-weight-bold" style="color: #5ac1cb">Itelma</span><br/>
                Made with <span class="text-red-accent-2 font-weight-bold">Faith in the Emperor</span>
              </div>

              <v-img width="50%" height="50%" class="mx-auto mt-5" :src="itelmaLogo"/>
            </div>

            <div class="pa-2 mb-16">
              <div class="text-body-2 text-center text-grey-lighten-1">* в разработке...</div>
            </div>
          </template>
        </v-navigation-drawer>

        <v-main style="min-height: 100vh" class="mt-13 mx-3">
          <router-view />
          <notifications position="bottom right" close-on-click :duration="3000"/>
        </v-main>
      </v-layout>
    </v-card>
  </v-app>
</template>
