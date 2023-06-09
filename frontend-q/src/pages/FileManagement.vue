<template>
  <div>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-9">
        <div v-if="loading || uploadingFiles" class="q-py-lg flex justify-center">
          <q-spinner-oval color="primary" size="3rem" />
        </div>
        <q-card v-else flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section class="q-pa-lg">
            <p class="text-h6 text-weight-bold">
              {{ $t('pages.FileManagementPage.title') }}
            </p>
            <q-select
              v-model="projectName"
              :placeholder="$t('pages.FileManagementPage.projectName')"
              class="q-mb-md"
              bg-color="accent"
              borderless
              :options="userProjects"
              option-value="name"
              option-label="name"
              emit-value
            />
          </q-card-section>
          <q-card-section class="q-pa-lg">
            <div v-if="projectName" class="flex justify-between">
              <div class="text-h6 text-weight-bold text-dark">
                {{ $t('pages.FileManagementPage.uploadFilesTitle') }}
              </div>
              <div class="text-h6 text-weight-bold text-dark">
                {{ projectName.name }}
              </div>
            </div>
            <div v-else class="flex justify-between">
              <div class="text-h6 text-weight-bold text-negative">
                {{ $t('pages.FileManagementPage.selectProjectTitle') }}
              </div>
            </div>
            <q-separator class="q-my-lg" />
            <div v-if="projectName && !loading" class="row q-col-gutter-md">
              <div
                v-for="(file, i) in projectFiles"
                :key="i"
                class="col-12 col-sm-6 col-md-4"
              >
                <div class="wrapper bg-accent">
                  <div
                    class="flex full-width justify-between items-center q-px-md q-py-sm"
                  >
                    <div>
                      <!-- Name -->
                      <div class="text-dark text-h6 text-weight-bold">
                        {{ file.split('.')[0] }}
                      </div>
                      <!-- Extension -->
                      <div class="text-dark-page text-body">
                        {{ file.split('.')[1] }}
                      </div>
                    </div>
                    <q-btn
                      round
                      color="negative"
                      unelevated
                      class="q-mx-xs"
                      icon="delete"
                      size="sm"
                      @click="deleteProjectFile(file)"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="text-center q-py-lg" v-if="projectFiles.length === 0">
              {{ $t('pages.FileManagementPage.noFound') }}
            </div>
            <q-btn
              v-if="projectName"
              unelevated
              color="primary"
              class="q-mt-md"
              text-color="white"
              @click="indexProject"
            >
              {{ $t('pages.FileManagementPage.indexBtn') }}
            </q-btn>
          </q-card-section>
        </q-card>
      </div>
      <div v-if="projectName" class="col-12 col-md-3">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 10px">
          <q-card-section class="q-pa-md">
            <div class="text-h6 text-weight-bold text-dark">
              {{ $t('pages.FileManagementPage.uploadNewFileTitle') }}
            </div>
            <q-separator class="q-my-lg" />
            <div v-if="uploadingFiles" class="q-py-lg flex justify-center">
              <q-spinner-oval color="primary" size="3rem" />
            </div>
            <div v-if="uploadingError" class="q-py-sm flex justify-center">
              <div class="text-h6 text-negative">
                {{ uploadingError }}
              </div>
            </div>
            <div v-if="success" class="q-py-sm flex justify-center">
              <div class="text-h6 text-primary">
                {{ success }}
              </div>
            </div>
            <!-- <q-btn
              unelevated
              color="bg-accent"
              class="full-width bg-accent"
              style="height: 200px"
              @click="loadLocalFiles"
              v-if="!uploadingFiles"
            >

            </q-btn> -->
            <p>Drag or Click to upload files</p>
            <q-file
              v-model="files"
              multiple
              append
              accept=".docx,.pdf,.html,.mp3,.m4a,.xlsx"
              type="file"
              class="q-my-md full-width bg-accent file-input"
              style="height: 200px"
              use-chips
              placeholder="Drag or Click to upload the files"
            >
              <template #default>
                <q-icon
                  v-if="!files"
                  name="add"
                  color="dark"
                  size="24"
                  class="add-btn"
                ></q-icon>
              </template>
            </q-file>

            <q-btn
              color="primary"
              unelevated
              class="text-capitalize q-mt-lg upload-nt"
              text-color="white"
              style="width: 140px"
              v-if="!uploadingFiles && files"
              @click="uploadFiles"
              icon="cloud_upload"
            >
              {{ $t('pages.FileManagementPage.uploadBtn') }}
            </q-btn>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue';
import { api } from 'src/boot/axios';
import { useProjectStore } from 'src/stores/project';
import { useAuthStore } from 'src/stores/auth';

import { useServiceStore } from 'src/stores/service';
import { useQuasar } from 'quasar';

const $q = useQuasar();
const serviceStore = useServiceStore();
const authStore = useAuthStore();

const filesRef = ref(null);
const store = useProjectStore();
const loading = ref(false);
const error = ref(null);
const uploadingFiles = ref(false);
const uploadingError = ref(null);
const success = ref(null);
const projectName = ref(store.selectedProject ? store.selectedProject : '');
const projectFiles = computed(() => store.projectFiles);
// const projectList = ref([]);
const userProjects = ref([]);
const files = ref(null);

const loadLocalFiles = async () => {
  // filesRef.value.click();
  console.log(files.value.length);
  await uploadFiles();
};
const fetchUserProjects = async () => {
  try {
    uploadingError.value = null;
    uploadingFiles.value = true;
    const res = await store.fetchUserProjects(authStore.user.id);
    userProjects.value = res;
  } catch (err) {
    console.log(err);
    uploadingError.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    uploadingFiles.value = false;
  }
};
const uploadFiles = async (e) => {
  loading.value = true;
  const formData = new FormData();
  for (var i = 0; i < files.value.length; i++) {
    let file = files.value[i];
    formData.append('files', file);
  }
  api
    .post(`file/upload?project_name=${projectName.value}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(function () {
      loading.value = false;
      listProjectFiles();
    })
    .catch(function () {
      error.value = err;
    });
};

const deleteProjectFile = async (file) => {
  try {
    error.value = null;
    loading.value = true;
    console.log('Delete Project');
    const res = await store.deleteProjectFile({
      project_name: projectName.value,
      filename: file,
    });
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
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
    store.projectFiles = [];
    listProjectFiles();
    getSessions();
  }
});
// const fetchProjects = async () => {
//   try {
//     error.value = null;
//     loading.value = true;
//     const res = await store.fetchProjects();
//     console.log(res);
//     var projects = res.filter(function (o1) {
//       return userProjects.value.some(function (o2) {
//         return o1.name === o2.name; // return the ones with equal id
//       });
//     });
//     projectList.value = projects;
//   } catch (err) {
//     console.log(err);
//     error.value = err.response.status + ' - ' + err.response.statusText;
//   } finally {
//     loading.value = false;
//   }
// };
const indexProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.indexProject({
      project_name: projectName.value,
    });
    if (res) {
      $q.notify({
        message: res.message,
        position: 'top-right',
        color: 'primary',
      });
    }
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
    } else {
      return;
    }
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
onMounted(async () => {
  await fetchUserProjects();
  await listProjectFiles();
  // await fetchProjects();
});
</script>
<style lang="scss"></style>
