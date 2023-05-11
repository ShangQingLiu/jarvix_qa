<template>
  <div class="col-12 col-md-6">
    <q-card flat class="bg-transparent q-px-none q-mb-lg">
      <q-card-section class="q-px-none">
        <div v-if="loading" class="q-py-lg flex justify-center">
          <q-spinner color="dark" size="3em" />
        </div>
        <div v-if="error" class="q-py-sm flex justify-center">
          <div class="text-h6 text-negative">
            {{ error }}
          </div>
        </div>
        <q-form @submit.prevent="createProject">
          <q-input
            borderless
            bg-color="white"
            v-model="projectName"
            placeholder="Project Name"
            class="q-mb-md"
            :input-style="{ padding: '0px 23px' }"
            required
          />
          <q-input
            borderless
            bg-color="white"
            v-model="description"
            placeholder="Type project description here..."
            type="textarea"
            class="q-mb-md"
            :input-style="{ padding: '20px 23px' }"
            required
          />
          <q-btn
            color="primary"
            unelevated
            class="text-capitalize"
            text-color="white"
            type="submit"
            >Create Project</q-btn
          >
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useProjectStore } from "src/stores/project";
const store = useProjectStore();
const projectName = ref("");
const description = ref("");
const loading = ref(false);
const error = ref(null);
const createProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.createProject({
      name: projectName.value,
      description: description.value,
    });
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}
</style>
