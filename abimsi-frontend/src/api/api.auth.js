import {apiClient} from "./api.base.js";

export async function login(email, password) {
  const response = await apiClient.post('/auth/login', {email: email, password: password});
  if (response.error)
    return false;

  localStorage.setItem('access_token', response.data.accessToken)
  localStorage.setItem('refresh_token', response.data.refreshToken)

  return true;
}

export async function profile() {
  const response = await apiClient.post('/auth/profile')
  return response.data
}

export async function refresh() {
  const response = await apiClient.post('/auth/refresh', {refresh_token: localStorage.getItem('refresh_token')});

  if (!response.error) {
    localStorage.setItem('access_token', response.data.accessToken)
    localStorage.setItem('refresh_token', response.data.refreshToken);

    return true;
  }

  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  return false;
}

export async function verify() {
  const response = await apiClient.post('/auth/verify')
  if (response.error)
    return false;

  return true;
}
