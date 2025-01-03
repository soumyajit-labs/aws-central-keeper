import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const api = axios.create({
  baseURL: "https://aws-central-keeper.onrender.com/"
});

const refreshAccessToken = async () => {
  try {
    const response = await axios.get("https://sso-gatekeeper.onrender.com/refresh", { withCredentials: true });
    const response_data = response?.data;
    console.log(response_data)
    if (response.status === 200) {
      if (response_data && response_data.access_token) {
        try {
          localStorage.setItem(ACCESS_TOKEN, response_data.access_token);
          console.log('Token refreshed & stored successfully');
          // window.location.href = '/landing';
        }
        catch (error) {
          console.error('Error while setting the access token:', response.status);
          // window.location.href = 'https://dev-63025152.okta.com/';
        }
      } else {
        console.error('Access token not in the response:', response.status);
        // window.location.href = 'https://dev-63025152.okta.com/';
      } 
    } else {
      console.error('Failed to refresh tokens:', response.status);
      // window.location.href = 'https://dev-63025152.okta.com/';
    }
  } catch (error) {
    console.error('Error refreshing tokens:', error);
    // window.location.href = 'https://dev-63025152.okta.com/';
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