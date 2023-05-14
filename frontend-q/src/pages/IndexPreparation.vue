<template>
  <div>
    <div class="row">
      <div class="col-12">
        <div class="row flex q-col-gutter-sm justify-between align-center">
          <div>
            <q-btn
              :color="panel === 'chat' ? 'primary' : 'white'"
              :text-color="panel === 'chat' ? 'white' : 'dark-page'"
              unelevated
              style="height: 55px"
              icon="img:/static/chat.svg"
              :label="$t('pages.IndexPreparation.chatBtn')"
              @click="panel = 'chat'"
            />
            <q-btn
              :color="panel === 'questions' ? 'primary' : 'white'"
              :text-color="panel === 'questions' ? 'white' : 'dark-page'"
              unelevated
              style="height: 55px"
              icon="img:/static/questions.svg"
              :label="$t('pages.IndexPreparation.validationForum')"
              @click="panel = 'questions'"
              class="q-ml-md"
            />
          </div>
          <div class="q-mb-md col-12 col-md-4">
            <q-select
              label="Choose Project"
              v-model="projectName"
              :placeholder="$t('pages.IndexPreparation.chooseProject')"
              bg-color="white"
              :options="projects"
              option-value="name"
              option-label="name"
              emit-value
              borderless
            />
          </div>
          <div
            class="q-mb-md col-12 col-md-4"
            v-if="sessions.length && showExistingSessions"
          >
            <q-select
              :label="$t('pages.IndexPreparation.chooseSession')"
              v-model="session"
              :placeholder="$t('pages.IndexPreparation.chooseSession')"
              class="q-mb-md col-12 col-md-4"
              bg-color="white"
              :options="sessions"
              borderless
            />
          </div>
          <div class="q-mb-md col-12 col-md-4" v-if="!showExistingSessions">
            <q-btn
              color="primary"
              @click="showExistingSessions = !showExistingSessions"
              style="height: 55px"
              unelevated
            >
              {{ $t('pages.IndexPreparation.showExistingSession') }}
            </q-btn>
          </div>
        </div>

        <q-tab-panels v-model="panel" class="bg-transparent q-px-none q-py-none">
          <q-tab-panel class="q-px-none q-py-none" name="chat">
            <Chat />
          </q-tab-panel>

          <q-tab-panel class="q-px-none" name="questions">
            <Questions />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Chat from '../components/IndexPreparation/Chat.vue';
import Questions from '../components/IndexPreparation/Questions.vue';
import { useProjectStore } from 'src/stores/project';
import { useAuthStore } from 'src/stores/auth';
import { useServiceStore } from 'src/stores/service';
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
const sessions = ref([]);
const showExistingSessions = ref(false);

watch(projectName, (projectValue) => {
  if (projectValue) {
    store.selectedProject = projectValue;
    getSessions();
  }
});
watch(session, (sessionValue) => {
  if (sessionValue) {
    serviceStore.selectedSession = sessionValue;
    getChatHistory();
  }
});
watch(panel, (panelValue, OldValue) => {
  if (panelValue !== OldValue) {
    serviceStore.selectedSession = null;
    serviceStore.chatHistory = [];
  }
});
const fetchUserProjects = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.fetchUserProjects(authStore.user.id);
    projects.value = res;
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
      sessions.value = res.sessions;
    } else {
      return;
    }
  } catch (err) {
    console.log(err);
    sessions.value = [];
    error.value = err.response.status + ' - ' + err.response.statusText;
    $q.notify({
      message: error.value ? error.value : 'Something Went Wrong',
      position: 'top-right',
      color: 'negative',
    });
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
  await getSessions();
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
