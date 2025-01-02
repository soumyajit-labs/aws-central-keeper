import axios from "axios";
const apiUrl = "/choreo-apis/mulecentral/backend/v1";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl
});

const refreshAccessToken = async () => {
  try {
    const response = await axios.post("https://sso-gatekeeper.onrender.com/refresh", { withCredentials: true });
    if (response.ok) {
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

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 403) {
      console.log("403 detected, attempting to refresh token...");
      try {
        await refreshAccessToken();
      } catch (refreshError) {
        console.error("Refresh token failed");
      }
    }
    return Promise.reject(error);
  }
);

export default api;