import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    user: null,
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
          await this.fetchUsers();
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
          console.log(data);
          this.user = data;
          localStorage.setItem("jarvixUser", JSON.stringify(data));
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
  },
});
