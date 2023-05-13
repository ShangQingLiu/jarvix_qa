<template>
  <div class="row q-col-gutter-md">
    <CreateProject v-if="authStore.user.role == 'Admin'" />
    <ProjectsList />
  </div>
</template>

<script setup>
import ProjectsList from "src/components/IndexPage/Index/ProjectsList.vue";
import CreateProject from "src/components/IndexPage/Index/CreateProject.vue";
import { useAuthStore } from "src/stores/auth";
const authStore = useAuthStore();
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
