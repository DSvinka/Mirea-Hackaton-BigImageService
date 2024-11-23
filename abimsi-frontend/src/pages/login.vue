<script setup>
import {login} from '@/api/api.auth'

import { useField, useForm } from 'vee-validate'
import {rules} from "@/plugins/rules";

const { handleSubmit } = useForm({
  email: rules.email,
  password: rules.password
})

const email = useField('email')
const password = useField('password')

const submit = handleSubmit(values => {
  login(values.email, values.password)
})
</script>

<template>
  <v-container class="d-flex justify-center align-center" style="height: 100vh" fluid>
    <v-card variant="outlined" class="d-flex justify-center align-center mx-auto w-50 pa-10">
      <v-form @submit.prevent="submit" class="w-100">
        <v-card-title class="mb-5 mx-auto text-center">Вход в Систему</v-card-title>
        <v-text-field
          v-model="email.value.value"
          :counter="320"
          :error-messages="email.errorMessage.value"
          label="Email"
        ></v-text-field>

        <v-text-field
          v-model="password.value.value"
          :error-messages="password.errorMessage.value"
          label="Пароль"
        ></v-text-field>

        <div class="d-flex justify-center align-center">
          <v-btn class="me-4" type="submit">
            Войти
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<style scoped lang="sass">

</style>
