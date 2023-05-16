import { boot } from "quasar/wrappers";
import axios from "axios";

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: "https://api.so-supreme.sis.ai/api/" });

// ℹ️ Add request interceptor to send the authorization header on each subsequent request after login
api.interceptors.request.use((config) => {
  console.log(config.url);
  // Retrieve token from localStorage
  const user = JSON.parse(localStorage.getItem("jarvixUser"));
  // If token is found
  if (user) {
    config.headers = config.headers || {};
    if (
      config.url !== "auth/login" ||
      config.url !== "user-management/forgot_password"
    ) {
      config.headers.Authorization = user ? `${user.access_token}` : "";
    }
  }
  return config;
});

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
