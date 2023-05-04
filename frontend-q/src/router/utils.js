/**
 * Return if user is logged in
 * This is completely up to you and how you want to store the token in your frontend application
 * e.g. If you are using cookies to store the application please update this function
 */
import { useAuthStore } from "src/stores/auth";

export const isUserLoggedIn = async () => {
  if (localStorage.getItem("jarvixUser")) {
    const userData = JSON.parse(localStorage.getItem("jarvixUser"));
    // user status checking
    const store = useAuthStore();
    if (Object.keys(store.user).length === 0 && !isTokenExpired(userData)) {
      await store.getLoggedInUserData();
    }
    return !isTokenExpired(userData);
  }
  return false;
};
export function isTokenExpired(userData) {
  if (userData) {
    const expiryTime = new Date(Date.now());
    const expiresAt = new Date(userData.exp * 1000);
    return expiresAt < expiryTime;
  }
  return true;
}
