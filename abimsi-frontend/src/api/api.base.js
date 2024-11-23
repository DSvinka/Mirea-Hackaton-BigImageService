import axios from "axios";

import router from '@/router';

import { useNotification } from "@kyvg/vue3-notification";
const { notify }  = useNotification()

export const apiUrl = import.meta.env.VITE_API_URL

export const apiClient = axios.create({
    baseURL: apiUrl,
    timeout: 5000,
    headers: {'X-Custom-Header': 'foobar', "authorization": "Bearer " + localStorage.getItem('access_token')},
});

apiClient.interceptors.response.use(successHandler, errorHandler);

function successHandler(response) {
    notify({type: "success", title: "Успех!"});
    return {data: response.data.data, error: response.data.error};
}

function errorHandler(error) {
    notify({type: "error", title: "Ошибка!", text: error.message});
    if (error.status === 401) {
      router.push('/login');
    }
    return {data: null, error: null, isError: true};
}
