import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useProjectStore = defineStore("projectStore", {
  state: () => ({
    projectsList: [],
    userProjects: [],
    projectFiles: [],
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
    sendProjectInvitation(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post(
            `project-management/${payload.projectId}/invite`,
            {
              email: payload.email,
            }
          );
          console.log(data);

          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    fetchUserProjects(userId) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get(`project-management/user/${userId}`);
          this.userProjects = data.projects;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    indexProject(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post(`file/prepareIndex`, {
            project_name: payload.project_name,
          });
          console.log(data);
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },

    listProjectFiles(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post(`file/list_files`, {
            project_name: payload.project_name,
          });
          this.projectFiles = data.files;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    checkProjectIndex(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post(`file/checkIndex`, {
            project_name: payload.project_name,
          });

          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    deleteProjectFile(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          console.log(payload);
          const { data } = await api.delete(`file/delete`, {
            filename: payload.filename,
            project_name: payload.project_name,
          });
          this.projectFiles = this.projectFiles.filter(
            (file) => file !== payload.filename
          );
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
