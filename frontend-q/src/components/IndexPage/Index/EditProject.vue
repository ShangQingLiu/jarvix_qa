<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">Edit Project</div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner color="dark" size="3em" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <q-form @submit.prevent="editProject">
      <q-input
        borderless
        bg-color="white"
        v-model="projectDataLocal.name"
        placeholder="Project Name"
        class="q-mb-md"
        :input-style="{ padding: '0px 23px' }"
        required
      />
      <q-input
        borderless
        bg-color="white"
        v-model="projectDataLocal.description"
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
        >Update Project</q-btn
      >
    </q-form>
  </div>
</template>
<script setup>
import { useProjectStore } from "src/stores/project";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router = useRouter();
const loading = ref(false);
const error = ref(null);
const store = useProjectStore();
const currentProject = store.projectsList.find(
  (project) => project.id == route.params.id
);
console.log(currentProject);
const projectData = {
  name: currentProject ? currentProject.name : "",
  description: currentProject ? currentProject.description : "",
};
const projectDataLocal = ref(structuredClone(projectData));
const editProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.editProject({
      form: {
        ...projectDataLocal.value,
      },
      projectId: route.params.id,
    });
    console.log(res);
    router.push("/");
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
