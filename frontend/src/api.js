import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const api = axios.create({
  baseURL: "https://aws-central-keeper.onrender.com/"
});

const refreshAccessToken = async () => {
  try {
    const response = await axios.get("https://sso-gatekeeper.onrender.com/refresh", { withCredentials: true });
    if (response.status === 200 && response.data.refresh) {
      localStorage.setItem(ACCESS_TOKEN, response.data.access_token);
      console.log('Tokens refreshed successfully');
      window.location.href = '/landing';
    } else {
      console.error('Failed to refresh tokens:', response.status);
      window.location.href = 'https://dev-63025152.okta.com/';
    }
  } catch (error) {
    console.error('Error refreshing tokens:', error);
    window.location.href = 'https://dev-63025152.okta.com/';
  }
};

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 403) {
      try {
        console.log("403 detected, attempting to refresh token...");
        await refreshAccessToken();
      } catch (refreshError) {
        console.log("403 detected, attempting to refresh token...");
        console.error("Refresh token failed");
      }
    }
    return Promise.resolve();
  }
);

export default api;