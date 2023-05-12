<template>
  <div class="col-12 col-md-6">
    <q-card flat class="bg-white q-mb-lg">
      <q-card-section>
        <div class="text-h6 text-weight-bold text-dark">User Projects</div>
        <q-separator class="q-my-lg" />
        <div v-if="loading" class="q-py-lg flex justify-center">
          <q-spinner color="dark" size="3em" />
        </div>
        <div v-if="error" class="q-py-sm flex justify-center">
          <div class="text-h6 text-negative">
            {{ error }}
          </div>
        </div>
        <q-list>
          <q-item
            v-for="(project, i) in projects"
            :key="i"
            class="q-py-none q-px-none list-item q-mb-lg"
          >
            <q-item-section>
              <q-item-label class="text-dark">
                {{ project.name }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-item v-if="projects.length === 0 && !loading">
            <q-item-section> No User Projects Found </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useProjectStore } from "src/stores/project";
import { useRoute } from "vue-router";
const store = useProjectStore();
const route = useRoute();
const projects = ref([]);
const loading = ref(false);
const error = ref(null);
const fetchUserProjects = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.fetchUserProjects(route.params.id);
    projects.value = res;
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
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
