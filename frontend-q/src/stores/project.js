import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useProjectStore = defineStore("projectStore", {
  state: () => ({
    projectsList: [],
  }),
  actions: {
    createProject(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const res = await api.post("project-management/", {
            name: form.name,
            description: form.description,
          });
          console.log(res);
          await this.fetchProjects();
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
    fetchProjects() {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get("project-management/projects");
          this.projectsList = data.projects;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    deleteProject(projectId) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.delete(`project-management/${projectId}`);
          console.log(data);
          this.projectsList = this.projectsList.filter(
            (project) => project.id != projectId
          );
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    editProject(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.put(
            `project-management/${payload.projectId}`,
            {
              ...payload.form,
            }
          );
          this.projectsList = this.projectsList.map((project) => {
            if (project.id == payload.projectId) {
              return data;
            }
            return project;
          });
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
