import { defineStore } from "pinia";
import { api } from "src/boot/axios";

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
  }),
  actions: {
    submitQuery(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const { data } = await api.post("service/query", {
            query: form.query,
            // Static Data for now
            project_name: "project",
            session_id: guidGenerator(),
          });
          this.chatHistory.push({ type: "bot-message", text: data });
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });
    },
    addUserMessage(message) {
      this.chatHistory.push({ type: "user-message", text: message });
    },
  },
});
