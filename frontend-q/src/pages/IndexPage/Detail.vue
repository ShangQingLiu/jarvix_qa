<template>
  <div class="row">
    <div class="col-12">
      <q-card flat class="">
        <q-card-section>
          <div class="text-h6 text-weight-bold text-dark">
            {{ currentProject && currentProject.name }}
          </div>
          <q-separator class="q-my-lg" />
          <p class="text-dark-page">
            {{ currentProject && currentProject.description }}
          </p>
          <q-separator class="q-my-lg" />
          <div class="q-my-md" style="height: 80px">
            <q-avatar
              v-for="n in 5"
              :key="n"
              size="50px"
              class="absolute"
              :style="`left: ${n * 40}px`"
            >
              <img :src="`https://cdn.quasar.dev/img/avatar${n + 1}.jpg`" />
            </q-avatar>
            <q-avatar
              color="primary"
              text-color="white"
              class="absolute numbered-avatar"
              size="54px"
              font-size="19px"
              :style="`left: ${6 * 40}px; border: 2px solid white;`"
            >
              <span>+3</span>
            </q-avatar>
          </div>
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="$router.push(`/invite/${$route.params.id}`)"
              >Invite people</q-btn
            >
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="$router.push(`/edit/${$route.params.id}`)"
              >Update Project</q-btn
            >
            <q-btn
              color="dark1"
              unelevated
              class="text-capitalize"
              text-color="white"
              @click="deleteProject"
              >Delete Project</q-btn
            >
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { useProjectStore } from "src/stores/project";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router = useRouter();
const store = useProjectStore();
const loading = ref(false);
const error = ref(null);
const currentProject = computed(() => {
  return store.projectsList.find((project) => project.id == route.params.id);
});
onMounted(() => {
  if (!currentProject.value) {
    router.push("/");
  }
});
const deleteProject = async () => {
  try {
    error.value = null;
    loading.value = true;
    console.log(route.params.id);
    const res = await store.deleteProject(route.params.id);
    console.log(res);
    router.push("/");
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

.numbered-avatar .q-avatar__content {
  width: 48px;
  height: 50px;
}
</style>
