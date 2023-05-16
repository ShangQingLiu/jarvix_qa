import { defineStore } from "pinia";
import { api } from "src/boot/axios";

function parseJwt(token) {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}
export const useAuthStore = defineStore("authStore", {
  state: () => ({
    user: {},
    usersList: [],
  }),
  actions: {
    registerUser(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const res = await api.post("user-management/user_list", {
            username: form.username,
            email: form.email,
            password: form.password,
          });
          console.log(res);
          // await this.fetchUsers();
          resolve(res);
        } catch (error) {
          reject(error);
        }
      });
    },
    loginUser(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post("auth/login", {
            username: form.username,
            password: form.password,
          });
          const parsedData = parseJwt(data.access_token);
          localStorage.setItem(
            "jarvixUser",
            JSON.stringify({ ...data, ...parsedData })
          );
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    fetchUsers() {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get("user-management/user_list");
          this.usersList = data;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    deleteUser(userId) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.delete(`user-management/${userId}`);
          this.usersList = this.usersList.filter((user) => user.id !== userId);
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    editUser(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.put(`user-management/${payload.userId}`, {
            ...payload.form,
          });
          this.usersList = this.usersList.map((user) => {
            if (user.id === payload.userId) {
              return data;
            }
            return user;
          });
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    getCode(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post(`user-management/forgot_password`, {
            email: payload.email,
          });
          console.log(data);
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    getLoggedInUserData() {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get(`user-management/info`);
          console.log(data);
          this.user = data;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
