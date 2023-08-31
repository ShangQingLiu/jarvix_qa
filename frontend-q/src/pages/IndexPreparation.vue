<template>
  <div>
    <!-- <div class="row flex-wrap q-py-md q-col-gutter-sm"> -->
    <!-- <div class="col-6 col-md-4">
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
      </div> -->
    <!-- <div v-if="projectName && existingChat.length > 0" class="col-6 col-md-4">
        <q-btn color="primary" @click="generateNewSession" unelevated class="full-width">
          {{ $t('pages.IndexPreparation.generateNewSession') }}
        </q-btn>
      </div> -->
    <!-- <div v-if="sessions.length && showExistingSessions" class="col-6 col-md-4">
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
      </div> -->

    <!-- <div v-if="!showExistingSessions && sessions.length > 0" class="col-6 col-md-4">
        <q-btn color="primary" @click="toggleShow" unelevated class="full-width">
          {{ $t('pages.IndexPreparation.showExistingSession') }}
        </q-btn>
      </div> -->
    <!-- </div> -->
    <div class="row">
      <div class="col-12 q-mb-md">
        <q-tabs
          indicator-color="transparent"
          v-model="panel"
          inline-label
          class="bg-transparent"
          align="left"
        >
          <q-tab class="custom-tab" name="chat" :label="$t('pages.IndexPreparation.chatBtn')" />
          <q-tab class="custom-tab" name="validation-forum" :label="$t('pages.IndexPreparation.validationForum')" />
        </q-tabs>
      </div>
      <div class="col-12 q-mb-md">
        <q-tabs
          indicator-color="transparent"
          @update:model-value="(id) => {
            if (panel === 'validation-forum') {
              serviceStore.selectedFileIdList = [id]
              return
            }

            const index = serviceStore.selectedFileIdList.indexOf(id);
            if (index === -1) {
              serviceStore.selectedFileIdList.push(id);
            } else {
              serviceStore.selectedFileIdList.splice(index, 1);
            }
          }"
          inline-label
          class="bg-transparent"
          align="left"
        >
          <q-tab
            v-for="(file, i) in projectFiles"
            class="custom-tab"
            :class="{
              'q-tab--active': serviceStore.selectedFileIdList.includes(file.id),
            }"
            :name="file.id"
            :label="file.name"
            :key="i"
            v-bind:disable="tabStatus"
          />
        </q-tabs>
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <q-tab-panels v-model="panel" class="bg-transparent q-px-none q-py-none">
          <q-tab-panel class="q-px-none q-py-none" name="chat">
            <div class="chat-wrapper bg-white q-py-md q-pl-md">
              <div class="row q-col-gutter-md">
                <div
                  class="col-12 col-md-3"
                  style="height: calc(100vh - 277px); overflow-y: auto"
                >
                  <q-btn
                    color="dark"
                    text-color="dark"
                    rounded
                    unelevated
                    icon="add"
                    outline
                    :label="$t('pages.IndexPreparation.generateNewSession')"
                    @click="generateNewSession"
                    class="q-mb-md"
                  />
                  <div class="text-dark q-mb-lg">{{ $t('Extra.existingSession') }}</div>
                  <div class="sessions-list">
                    <div
                      class="text-subtitle2 q-mb-md"
                      v-for="session in sessions"
                      :key="session"
                      @click="serviceStore.selectedSession = session"
                      :class="[
                        serviceStore.selectedSession === session
                          ? 'text-dark'
                          : 'text-dark-page',
                      ]"
                      style="cursor: pointer"
                    >
                      {{ session }}
                    </div>
                  </div>
                  <!-- {{ sessions }} -->
                </div>
                <div class="col-12 col-md-9">
                  <div class="q-px-md border-left">
                    <Chat @disabled="filesStatus" />
                  </div>
                </div>
              </div>
            </div>
          </q-tab-panel>
          <!-- 90 + 98 + 128 -->
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
// const projectName = ref(store.selectedProject ? store.selectedProject : '');
const projectName = computed(() => store.selectedProject);

const loading = ref(false);
const error = ref(null);
const projects = ref([]);
const authStore = useAuthStore();
const session = ref(serviceStore.selectedSession ? serviceStore.selectedSession : null);
const sessions = computed(() => serviceStore.sessions);
const showExistingSessions = computed(() => serviceStore.showExistingSessions);
const existingChat = computed(() => serviceStore.chatHistory);
const projectFiles = computed(() => store.projectFiles);
const tabStatus = ref(false);

const filesStatus = (status) => {
  tabStatus.value = status
}
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
    serviceStore.chatHistory = [];
    store.selectedProject = projectValue;
    store.chatHistory = [];
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
    serviceStore.selectedFileIdList = []
  }
});
serviceStore.$subscribe((mutation, state) => {
  session.value = state.selectedSession;
});
const generateNewSession = async () => {
  let sessionFrom = panel.value === 'chat' ? 'ChatRoom' : 'ValidationForum';
  console.log(sessionFrom);

  serviceStore.sessionFrom = sessionFrom;
  let sessionId = guidGenerator();
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
    console.log(res);
    // const indexedProjects = await store.getIndexedProjects();
    // const filteredProjects = res.filter((project, index) => {
    //   if (indexedProjects[index].message === 'Index exists') {
    //     return project;
    //   }
    // });
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
  await getSessions();
  if (serviceStore.selectedSession) {
    await getChatHistory();
  }
  await listProjectFiles();
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
.q-tab.custom-tab {
  border: 1px solid #878787;
  border-radius: 100px;
  margin-right: 10px;
}
.custom-tab.q-tab--active {
  background: $primary;
  color: #fff;
  border: 1px solid $primary;
}
.chat-wrapper {
  border-radius: 20px;
}
.border-left {
  border-left: 1px solid #000;
}
</style>

<style lang="scss">
.q-tab-panels .scroll {
  // overflow: hidden !important;
}
</style>
