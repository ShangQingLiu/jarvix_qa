<template>
  <div class="container mt-4">
  <!-- Add this header element to contain the logo -->
  <header class="header d-flex justify-content-center align-items-center">
      <!-- Add your SVG logo using the img tag -->
      <img class="logo" src="@/assets/Synergies_logo.svg" alt="Logo" />
    </header>
    <h1 class="text-center mb-4">Jarvix Robot</h1>
    <div class="card">
      <div class="card-body">
        <form>
          <div class="mb-3">
            <label for="project-name" class="form-label">Project Name:</label>
            <input
              class="form-control"
              id="project-name"
              type="text"
              v-model="projectName"
            />
          </div>
          <h3 class="mt-3">Uploaded Files</h3>
          <ul class="list-group">
            <li class="list-group-item" v-for="file in files" :key="file">{{ file }}</li>
          </ul>
          <button
            class="btn btn-info mt-3"
            type="button"
            @click="listFiles"
          >
            Refresh File List
          </button>

          <div class="mb-3">
            <input class="form-control" type="file" @change="selectFile" />
          </div>
          <button
            class="btn btn-primary"
            type="button"
            v-if="selectedFile"
            @click="uploadFile"
          >
            Confirm Upload
          </button>
          <button
            class="btn btn-secondary"
            type="button"
            v-if="projectName"
            @click="prepareIndex"
          >
            Prepare Index
          </button>
          <div class="mb-3">
            <label for="session-id" class="form-label">Session ID:</label>
            <input class="form-control" id="session-id" type="text" v-model="sessionID" />
          </div>
          <div v-if="sessionID">
            <h3 class="mt-3">Session ID: {{ sessionID }}</h3>
            <pre>{{ results }}</pre>
          </div>
        </form>
        <div class="mt-4">
          <div class="mb-3">
            <label for="query" class="form-label">Query:</label>
            <input
              class="form-control"
              id="query"
              type="text"
              v-model="query"
            />
          </div>
          <button
            class="btn btn-success"
            type="button"
            @click="submitQuery"
          >
            Submit Query
          </button>
        </div>
        <div class="chat-history mt-4">
          <div
            class="chat-message"
            v-for="message in chatHistory"
            :key="message.id"
            :class="message.type"
          >
            <pre class="message-text">{{ message.text }}</pre>
          </div>
        </div>
        <button class="btn btn-danger mt-2" @click="cleanHistory">Clean History</button>
      </div>
    </div>
  </div>
</template>



<script>
import axios from "axios";

export default {
  data() {
    return {
      projectName: "",
      files: [],
      selectedFile: null,
      sessionID: null,
      results: null,
      query: "", 
      answer: null, 
      chatHistory: [],
    };
  },
  methods: {
    cleanHistory() {
    this.chatHistory = [];
  },
    selectFile(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile || !this.projectName) {
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("project_name", this.projectName);

      try {
        const response = await axios.post("/api/upload", formData);
        this.sessionID = response.data.session_id;
        this.selectedFile = null;
      } catch (error) {
        console.error("File upload failed:", error);
      }
    },
    async prepareIndex() {
  if (!this.projectName) {
    return;
  }

  try {
    console.log("Preparing index...", this.projectName);
    const formData = new FormData();
    formData.append("project_name", this.projectName);
    const response = await axios.post("/api/prepareIndex", formData);
    console.log("Index prepared successfully:", response.data);
  } catch (error) {
    console.error("Failed to prepare index:", error);
    }
  },

    async submitQuery() {
    console.log(this.projectName, this.sessionID, this.query);
  if (!this.projectName || !this.sessionID || !this.query) {
    return;
  }

  try {
    this.chatHistory.push({ type: 'user-message', text: this.query });

    const response = await axios.post(
      `/api/query`,
      {
        project_name: this.projectName,
        session_id: this.sessionID,
        query: this.query
      },
      {
        timeout: 300000 // Set the timeout to 5 minutes (300000 ms)
      }
    );
    this.answer = response.data;
    // this.chatHistory.push({ type: 'user-message', text: this.query });
    this.chatHistory.push({ type: 'bot-message', text: this.answer });
  } catch (error) {
    console.error("Failed to submit query:", error);
  }
},
async listFiles() {
    if (!this.projectName) {
      return;
    }

    try {

      const formData = new FormData();
      formData.append("project_name", this.projectName);
      const response = await axios.post("/api/list_files", formData);
      this.files = response.data.files;
    } catch (error) {
      console.error("Failed to list files:", error);
    }
  },

  },

};
</script>


<style scoped>
/* Color Palette */
/* #4EB3B3 */
/* #047171 */
/* #DCDDDD */
/* #626463 */
/* #313232 */

body {
  background-color: #DCDDDD;
}

h1 {
  color: #047171;
}

.card {
  background-color: #4EB3B3;
  border-color: #047171;
}

.card-body {
  background-color: #626463;
  color: #DCDDDD;
}

.form-label {
  color: #DCDDDD;
}

.form-control {
  background-color: #DCDDDD;
  color: #313232;
  border-color: #313232;
}

.btn-primary {
  background-color: #047171;
  border-color: #047171;
}

.btn-secondary {
  background-color: #313232;
  border-color: #313232;
}

.btn-info {
  background-color: #4EB3B3;
  border-color: #4EB3B3;
}

.btn-success {
  background-color: #4EB3B3;
  border-color: #4EB3B3;
}

.chat-history {
  background-color: #313232;
  padding: 1rem;
  border-radius: 5px;
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}


.chat-message {
  margin-bottom: 1rem;
  word-wrap: break-word;
  font-size: 1.5rem;
}

.user-message .message-text,
.bot-message .message-text {
  font-size: 1.5rem;
  color: #DCDDDD;
  text-align: left;
  white-space: pre-wrap; /* Preserves white spaces and wraps text */
  word-break: break-word; /* Breaks long words if necessary */
}

.user-message .message-text {
  color: #4EB3B3;
  text-align: right;
}
.header {
  width: 100%;
  height: 100px;
  /* background-color: #4EB3B3; */
}

/* You can customize the logo styles if necessary */
.logo {
  width: 200px;
  height: 200px;
}

</style>
