import { defineStore } from "pinia";
import { api, apiFetch } from "src/boot/axios";
import { useProjectStore } from "src/stores/project";
import { guidGenerator } from "src/utils";

export const useServiceStore = defineStore("ServiceStore", {
  state: () => ({
    chatHistory: [],
    sessions: [],
    selectedSession: null,
    sessionId: null,
    showExistingSessions: false,
    currentLanguage: "EN",
    sessionFrom: "ChatRoom",
    validationQuestions: [],
    validationForumContent: null,
    selectedFileIdList: [],
  }),
  actions: {
    submitQuery(form, scrollToBottom) {
      return new Promise(async (resolve, reject) => {
        try {
          const store = useProjectStore();
          if (store.selectedProject) {
            if (!this.sessionId) {
              this.sessionId = guidGenerator();
            }

            const index = this.chatHistory.length;
            this.chatHistory.push({
              query: form.query,
              response: '...'
            });
            const record = this.chatHistory[index];
            await scrollToBottom?.()


            const delay = (ms) => new Promise((res) => setTimeout(res, ms));
            await apiFetch("service/query/stream", {
              method: 'POST',
              body: JSON.stringify({
                query: form.query,
                project_name: store.selectedProject,
                session_id: this.sessionId,
                language: this.currentLanguage,
                fileIdList: this.selectedFileIdList,
              }),
              responseType: 'stream',
            })
              .then((stream) => {
                const reader = stream
                  .pipeThrough(new TextDecoderStream())
                  .getReader()

                record.response = ''

                const processText = async ({ done, value: rawValue }) => {
                  if (done) {
                    return;
                  }
                  const textList = rawValue.slice(5).split("\n\ndata:")

                  for (const text of textList) {
                    record.response += text
                    await scrollToBottom?.()
                    await delay(100)
                  }

                  // Call processText recursively on next chunk
                  return reader.read().then(processText);
                }

                return reader.read().then(processText)
              })

            this.selectedSession = this.sessionId;
            // await this.getSessions();
            // await this.getChatHistory();
            resolve(record.response);
          } else {
            reject(new Error("Something Wrong"));
          }
        } catch (error) {
          reject(error);
        }
      });
    },
    addUserMessage(message) {
      this.chatHistory.push({ text: message });
    },
    getSessions() {
      return new Promise(async (resolve, reject) => {
        const store = useProjectStore();
        try {
          console.log(store.selectedProject);

          // If don't have any project nothing todo
          if (store.selectedProject) {
            const { data } = await api.get(
              `service/sessions/${store.selectedProject}`
            );
            // this.chatHistory.push({ type: "bot-message", text: data });
            console.log(data);
            this.sessions = data.sessions;
            this.selectedSession = data.sessions[this.sessions.length - 1];
            this.sessionId = data.sessions[this.sessions.length - 1];

            resolve(data);
          } else {
            this.sessions = [];
            reject(new Error("Something Wrong"));
          }
        } catch (error) {
          this.sessions = [];
          // If there are no session then
          // this.sessionId = guidGenerator()
          // store.selectedProject +
          // "-" +
          // this.sessionFrom +
          // "-" +
          // guidGenerator(this.sessionId);
          this.sessions.push(this.sessionId);
          this.selectedSession = this.sessionId;
          reject(error);
        }
      });
    },
    getChatHistory() {
      return new Promise(async (resolve, reject) => {
        try {
          const store = useProjectStore();

          if (this.selectedSession) {
            const { data } = await api.get(
              `service/chat_history/${store.selectedProject}/${this.selectedSession}`
            );
            this.chatHistory = data.chat_history;
            resolve(data);
          } else {
            const { data } = await api.get(
              `service/chat_history/${store.selectedProject}/${this.sessionId}`
            );
            this.chatHistory = data.chat_history;
            resolve(data);
          }
          // this.chatHistory.push({ type: "bot-message", text: data });
        } catch (error) {
          this.chatHistory = [];
          reject(error);
        }
      });
    },
    submitValidationForum(form) {
      return new Promise(async (resolve, reject) => {
        try {
          const store = useProjectStore();
          if (store.selectedProject) {
            if (!this.sessionId) {
              this.sessionId =
                // store.selectedProject +
                // "-" +
                // this.sessionFrom +
                // "-" +
                guidGenerator();
            }
            const { data } = await api.post("service/validation_form", {
              validation_form: form.query,
              project_name: store.selectedProject,
              // Same as Project Name to avoid conflicts
              session_id: this.sessionId,
              fileIdList: this.selectedFileIdList,
            });
            this.selectedSession = this.sessionId;
            await this.getSessions();
            this.validationForumContent = data;
            console.log(data);
            resolve(data);
          } else {
            reject(new Error("Something Wrong"));
          }
        } catch (error) {
          reject(error);
        }
      });
    },
  },
});
