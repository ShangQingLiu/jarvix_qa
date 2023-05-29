import { defineStore } from "pinia";
import { api } from "src/boot/axios";
import { useAuthStore } from "src/stores/auth";

export const useProjectStore = defineStore("projectStore", {
  state: () => ({
    projectsList: [],
    userProjects: [],
    projectFiles: [],
    selectedProject: null,
    projectUsers: [],
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
          const authStore = useAuthStore();
          await this.fetchProjects();
          await this.fetchUserProjects(authStore.user.id);
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
          resolve(data.projects);
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
          this.userProjects = this.userProjects.filter(
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
              role: payload.role,
              language: payload.language,
            }
          );
          console.log(data);

          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    invitePeople(payload) {
      const invitations = payload.inviteContent.map((invite) => {
        return this.sendProjectInvitation({
          projectId: payload.projectId,
          email: invite.email,
          role: invite.role,
          language: payload.language,
        });
      });
      return Promise.all(invitations);
    },
    fetchUserProjects(userId) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get(`project-management/user/${userId}`);
          console.log(data);
          this.userProjects = data;
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
            project_name: payload,
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
            data: {
              filename: payload.filename,
              project_name: payload.project_name,
            },
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
    async getIndexedProjects() {
      const projects = this.userProjects.map((p) => {
        return this.checkProjectIndex(p.name);
      });
      return Promise.all(projects);
    },
    fetchProjectUsers(projectId) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get(
            `project-management/${projectId}/users`
          );
          console.log(data);
          this.projectUsers = data;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    deleteProjectUser(payload) {
      return new Promise(async (resolve, reject) => {
        try {
          console.log(payload);
          const { data } = await api.delete(
            `project-management/${payload.projectId}/user/${payload.userId}/remove`
          );
          this.projectUsers = this.projectUsers.filter(
            (user) => payload.userId !== user.id
          );
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
