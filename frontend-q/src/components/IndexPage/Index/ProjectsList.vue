<template>
  <div class="col-12 col-md-6">
    <q-card flat class="bg-white q-mb-lg">
      <q-card-section>
        <div class="text-h6 text-weight-bold text-dark">
          {{ $t('pages.IndexPage.Index.ProjectList.title') }}
        </div>
        <q-separator class="q-my-lg" />
        <div v-if="loading" class="q-py-lg flex justify-center">
          <q-spinner-oval color="primary" size="3rem" />
        </div>
        <div v-if="error" class="q-py-sm flex justify-center">
          <div class="text-h6 text-negative">
            {{ error }}
          </div>
        </div>
        <q-list>
          <q-item
            v-for="(project, i) in projects.slice(0, numberOfProjectsToShow)"
            :key="i"
            class="q-py-none q-px-none list-item q-mb-lg"
          >
            <q-item-section>
              <q-item-label class="text-dark">
                {{ project.name }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <div class="flex">
                <q-btn
                  round
                  color="primary"
                  unelevated
                  class="q-mx-xs"
                  icon="visibility"
                  @click="$router.push(`/${project.id}`)"
                  size="sm"
                />
                <q-btn
                  round
                  color="primary"
                  unelevated
                  class="q-mx-xs"
                  icon="edit_square"
                  @click="$router.push(`/edit/${project.id}`)"
                  size="sm"
                  v-if="authStore.user.role == 'Admin'"
                />
                <q-btn
                  round
                  color="negative"
                  unelevated
                  class="q-mx-xs"
                  icon="delete"
                  v-if="authStore.user.role == 'Admin'"
                  @click="deleteConfirmationModal(project.id, project.name)"
                  size="sm"
                />
              </div>
            </q-item-section>
          </q-item>
          <q-item v-if="projects.length === 0">
            <q-item-section>
              {{ $t('pages.IndexPage.Index.ProjectList.noFound') }}
            </q-item-section>
          </q-item>
        </q-list>
        <q-separator class="q-my-lg" />
        <q-item-label
          @click="numberOfProjectsToShow = projects.length"
          v-if="projects.length >= 10 && numberOfProjectsToShow !== projects.length"
          header
          class="text-primary cursor-pointer q-pl-none"
        >
          {{ $t('pages.IndexPage.Index.ProjectList.viewAll') }}
        </q-item-label>
        <q-item-label
          @click="numberOfProjectsToShow = 10"
          v-if="numberOfProjectsToShow == projects.length"
          header
          class="text-primary cursor-pointer q-pl-none"
        >
          {{ $t('pages.IndexPage.Index.ProjectList.viewLess') }}
        </q-item-label>
      </q-card-section>
    </q-card>
    <q-dialog v-model="confirmDelete">
      <q-card class="bg-primary text-white q-pa-xl">
        <q-card-section style="margin-bottom: 50px">
          <div class="text-h6 text-center q-mb-xl">Warning!</div>
          <div class="text-h6 text-center">Do you really want to delete it?</div>
        </q-card-section>

        <q-card-actions align="center">
          <q-btn
            rounded
            padding="12px 50px"
            label="No"
            class="bg-white text-dark"
            v-close-popup
          />
          <q-btn
            rounded
            padding="12px 50px"
            label="Yes"
            class="bg-white text-dark"
            v-close-popup
            @click="deleteProject()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useProjectStore } from 'src/stores/project';
import { useAuthStore } from 'src/stores/auth';

const store = useProjectStore();
const projects = computed(() => store.userProjects);
const loading = ref(false);
const error = ref(null);
const numberOfProjectsToShow = ref(10);
const authStore = useAuthStore();
const confirmDelete = ref(false);
const projectId = ref(0);
const projectName = ref(0);



const fetchUserProjects = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.fetchUserProjects(authStore.user.id);
    // projects.value = res;
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const deleteProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    console.log(projectId.value);
    const res = await store.deleteProject(projectId.value, projectName.value);
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const deleteConfirmationModal = (id, name) => {
  confirmDelete.value = !confirmDelete.value;
  projectId.value = id;
  projectName.value = name
};
onMounted(async () => {
  // await fetchProjects();
  await fetchUserProjects();
});
</script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}
.list-item {
  .q-item__label {
    font-style: normal;
    font-weight: 600;
    font-size: 19px;
    line-height: 19px;
  }
  .q-item__label--caption {
    font-style: normal;
    font-weight: 400;
    font-size: 17px;
    line-height: 21px;
    color: $dark-page;
  }
}
</style>
