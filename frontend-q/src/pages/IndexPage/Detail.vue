<template>
  <div class="row">
    <div class="col-12">
      <q-card flat class="">
        <q-card-section v-if="loading">
          <div class="q-py-lg flex justify-center">
            <q-spinner-oval color="primary" size="2rem" />
          </div>
        </q-card-section>
        <q-card-section v-else>
          <div class="text-h6 text-weight-bold text-dark">
            {{ currentProject && currentProject.name }}
          </div>
          <q-separator class="q-my-lg" />
          <p class="text-dark-page">
            {{ currentProject && currentProject.description }}
          </p>
          <q-separator class="q-my-lg" />
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="$router.push(`/invite/${$route.params.id}`)"
              v-if="authStore.user.role == 'Admin'"
            >
              {{ $t('pages.IndexPage.Detail.inviteBtn') }}
            </q-btn>
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="$router.push(`/edit/${$route.params.id}`)"
              v-if="authStore.user.role == 'Admin'"
            >
              {{ $t('pages.IndexPage.Detail.updateBtn') }}
            </q-btn>
            <q-btn
              color="dark1"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="indexProject"
              v-if="authStore.user.role == 'Admin' && projectFiles.length != 0"
            >
              {{ $t('pages.IndexPage.Detail.indexBtn') }}
            </q-btn>
            <q-btn
              color="negative"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="deleteProject"
              v-if="authStore.user.role == 'Admin'"
            >
              {{ $t('pages.IndexPage.Detail.deleteBtn') }}
            </q-btn>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <ProjectUsers v-if="authStore.user.role == 'Admin'" />
  </div>
</template>

<script setup>
import { useProjectStore } from 'src/stores/project';
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import ProjectUsers from 'src/components/IndexPage/Detail/ProjectUsers.vue';

const $q = useQuasar();
const route = useRoute();
const router = useRouter();
const store = useProjectStore();
const loading = ref(false);
const error = ref(null);
const indexExist = ref(false);
const projectFiles = ref([]);
const authStore = useAuthStore();

const currentProject = computed(() =>
  store.userProjects.find((project) => project.id == route.params.id)
);
onMounted(async () => {
  const p = store.userProjects.find((project) => project.id == route.params.id);
  console.log(p);
  if (!currentProject.value) {
    router.push('/');
  }
  await listProjectFiles();
  // await checkProjectIndex();
});
const deleteProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    console.log(route.params.id);
    const res = await store.deleteProject(route.params.id);
    console.log(res);
    router.push('/');
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const indexProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.indexProject({
      project_name: currentProject.value.name,
    });
    if (res) {
      $q.notify({
        message: res.message,
        position: 'top-right',
        color: 'primary',
      });
      router.push('/');
    }
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
      project_name: currentProject.value.name,
    });

    projectFiles.value = res.files;
    console.log(res.files.length);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const checkProjectIndex = async () => {
  try {
    const res = await store.checkProjectIndex({
      project_name: currentProject.value.name,
    });
    console.log(res);
    if (res.message === 'Index exists') {
      indexExist.value = true;
      await listProjectFiles();
    }
  } catch (err) {
    console.log(err);
  }
};
const deleteProjectFile = async (file) => {
  try {
    error.value = null;
    loading.value = true;
    console.log('Delete Project');
    const res = await store.deleteProjectFile({
      project_name: currentProject.value.name,
      filename: file,
    });
    console.log(res);
    router.push('/');
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}

.numbered-avatar .q-avatar__content {
  width: 48px;
  height: 50px;
}
</style>
