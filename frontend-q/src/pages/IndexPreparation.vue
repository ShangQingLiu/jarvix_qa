<template>
  <div>
    <div class="row flex-wrap q-py-md q-col-gutter-sm">
      <div class="col-6 col-md-4">
        <q-btn
          :color="panel === 'chat' ? 'primary' : 'white'"
          :text-color="panel === 'chat' ? 'white' : 'dark-page'"
          unelevated
          style="height: 55px"
          icon="img:/static/chat.svg"
          :label="$t('pages.IndexPreparation.chatBtn')"
          @click="panel = 'chat'"
          class="full-width"
        />
      </div>
      <div class="col-6 col-md-4">
        <q-btn
          :color="panel === 'validation-forum' ? 'primary' : 'white'"
          :text-color="panel === 'validation-forum' ? 'white' : 'dark-page'"
          unelevated
          style="height: 55px"
          icon="img:/static/questions.svg"
          :label="$t('pages.IndexPreparation.validationForum')"
          @click="panel = 'validation-forum'"
          class="full-width"
        />
      </div>
      <div class="col-6 col-md-4">
        <q-select
          :label="$t('pages.IndexPreparation.chooseProject')"
          v-model="projectName"
          :placeholder="$t('pages.IndexPreparation.chooseProject')"
          bg-color="white"
          :options="projects"
          option-value="name"
          option-label="name"
          style="min-width: 160px"
          emit-value
          borderless
          class="full-width"
        />
      </div>
      <div v-if="projectName && existingChat.length > 0" class="col-6 col-md-4">
        <q-btn color="primary" @click="generateNewSession" unelevated class="full-width">
          {{ $t('pages.IndexPreparation.generateNewSession') }}
        </q-btn>
      </div>
      <div v-if="sessions.length && showExistingSessions" class="col-6 col-md-4">
        <q-select
          :label="$t('pages.IndexPreparation.chooseSession')"
          v-model="session"
          :placeholder="$t('pages.IndexPreparation.chooseSession')"
          style="min-width: 160px"
          bg-color="white"
          :options="sessions"
          borderless
          class="full-width"
        />
      </div>

      <div v-if="!showExistingSessions && sessions.length > 0" class="col-6 col-md-4">
        <q-btn color="primary" @click="toggleShow" unelevated class="full-width">
          {{ $t('pages.IndexPreparation.showExistingSession') }}
        </q-btn>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <q-tab-panels v-model="panel" class="bg-transparent q-px-none q-py-none">
          <q-tab-panel class="q-px-none q-py-none" name="chat">
            <Chat />
          </q-tab-panel>

          <!-- <q-tab-panel class="q-px-none" name="questions">
            <Questions />
          </q-tab-panel> -->
          <q-tab-panel class="q-px-none" name="validation-forum">
            <ValidationForum />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import Chat from '../components/IndexPreparation/Chat.vue';
// import Questions from '../components/IndexPreparation/Questions.vue';
import ValidationForum from '../components/IndexPreparation/ValidationForum.vue';

import { useProjectStore } from 'src/stores/project';
import { useAuthStore } from 'src/stores/auth';
import { useServiceStore } from 'src/stores/service';
import { guidGenerator } from 'src/utils';
import { useQuasar } from 'quasar';
const $q = useQuasar();

const serviceStore = useServiceStore();
const store = useProjectStore();
const panel = ref('chat');
const projectName = ref(store.selectedProject ? store.selectedProject : '');
const loading = ref(false);
const error = ref(null);
const projects = ref([]);
const authStore = useAuthStore();
const session = ref(serviceStore.selectedSession ? serviceStore.selectedSession : null);
const sessions = computed(() => serviceStore.sessions);
const showExistingSessions = computed(() => serviceStore.showExistingSessions);
const existingChat = computed(() => serviceStore.chatHistory);

const toggleShow = () => {
  serviceStore.showExistingSessions = !serviceStore.showExistingSessions;
};
const listProjectFiles = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.listProjectFiles({
      project_name: projectName.value,
    });
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
watch(projectName, (projectValue) => {
  if (projectValue) {
    store.selectedProject = projectValue;
    listProjectFiles();
    getSessions();
  }
});
watch(session, async (sessionValue) => {
  if (sessionValue) {
    serviceStore.selectedSession = sessionValue;
    serviceStore.sessionId = sessionValue;
    await getChatHistory();
  }
});
watch(panel, (panelValue, OldValue) => {
  if (panelValue !== OldValue) {
    serviceStore.selectedSession = null;
    serviceStore.chatHistory = [];
    console.log(panelValue);
    let sessionFrom = panelValue === 'chat' ? 'ChatRoom' : 'ValidationForum';
    serviceStore.sessionFrom = sessionFrom;
  }
});
serviceStore.$subscribe((mutation, state) => {
  session.value = state.selectedSession;
});
const generateNewSession = async () => {
  let sessionFrom = panel.value === 'chat' ? 'ChatRoom' : 'ValidationForum';
  console.log(sessionFrom);

  serviceStore.sessionFrom = sessionFrom;
  let sessionId = store.selectedProject + '-' + sessionFrom + '-' + guidGenerator();
  serviceStore.sessionId = sessionId;
  session.value = sessionId;
  serviceStore.chatHistory = [];
  serviceStore.sessions.push(sessionId);
  // await getSessions();
};
const fetchUserProjects = async () => {
  try {
    error.value = null;
    loading.value = true;

    const res = await store.fetchUserProjects(authStore.user.id);
    const indexedProjects = await store.getIndexedProjects();
    const filteredProjects = res.filter((project, index) => {
      if (indexedProjects[index].message === 'Index exists') {
        return project;
      }
    });
    projects.value = filteredProjects;
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const getSessions = async () => {
  try {
    error.value = null;
    loading.value = true;
    if (store.selectedProject) {
      const res = await serviceStore.getSessions();
      // sessions.value = res.sessions;
    } else {
      return;
    }
  } catch (err) {
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const getChatHistory = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await serviceStore.getChatHistory();
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
onMounted(async () => {
  await fetchUserProjects();
  if (serviceStore.selectedSession) {
    await getChatHistory();
  }
});
</script>
<style lang="scss" scoped>
.img-container {
  border-radius: 20px 20px 0px 0px;
  img {
    border-radius: 20px 20px 0px 0px;
  }
  position: relative;
  .menu-icon {
    position: absolute;
    top: 10px;
    right: 10px;
  }
}
</style>
