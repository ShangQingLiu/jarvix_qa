import { defineStore } from "pinia";
import { api } from "src/boot/axios";
import { useProjectStore } from "src/stores/project";

function guidGenerator() {
  var S4 = function () {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
  };
  return (
    S4() +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    S4() +
    S4()
  );
}
export const useServiceStore = defineStore("ServiceStore", {
  state: () => ({
    chatHistory: [],
    sessions: [],
    selectedSession: null,
  }),
  actions: {
    submitQuery(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const store = useProjectStore();
          if (store.selectedProject) {
            const { data } = await api.post("service/query", {
              query: form.query,
              project_name: store.selectedProject,
              // Same as Project Name to avoid conflicts
              session_id: store.selectedProject,
            });
            // this.chatHistory.push({ type: "bot-message", text: data });
            await this.getChatHistory();
            resolve(data);
          } else {
            reject(new Error("Something Wrong"));
          }
        } catch (error) {
          reject(error);
        }
      });
    },
    addUserMessage(message) {
      this.chatHistory.push({ type: "user-message", text: message });
    },
    getSessions() {
      return new Promise(async (resolve, reject) => {
        try {
          const store = useProjectStore();
          if (store.selectedProject) {
            const { data } = await api.get(
              `service/sessions/${store.selectedProject}`
            );
            // this.chatHistory.push({ type: "bot-message", text: data });
            console.log(data);
            this.sessions = data.sessions;
            resolve(data);
          } else {
            reject(new Error("Something Wrong"));
          }
        } catch (error) {
          reject(error);
        }
      });
    },
    getChatHistory() {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.get(
            `service/chat_history/${this.selectedSession}`
          );
          // this.chatHistory.push({ type: "bot-message", text: data });
          this.chatHistory = data.chat_history;
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
