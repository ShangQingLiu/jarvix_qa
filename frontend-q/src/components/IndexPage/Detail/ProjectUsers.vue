<template>
  <div class="col-12">
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner-oval color="primary" size="3rem" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <div class="q-py-lg q-gutter-sm">
      <q-avatar
        v-for="(user, i) in users.slice(0, numberOfUsersToShow)"
        :key="i"
        size="50px"
        class="overlapping"
        :style="`left: -${i * 20}px`"
        color="primary"
        text-color="white"
      >
        <img v-if="user.img" :src="user.img" />
        <template v-else>
          {{ user.username.charAt(0).toUpperCase() }}
        </template>
        <q-badge
          @click="deleteProjectUser(user.id)"
          style="min-height: 22px"
          floating
          color="negative"
        >
          <q-icon name="close" size="10px"></q-icon>
        </q-badge>
        <q-tooltip anchor="bottom middle" self="top middle" :offset="[10, 10]">
          <strong>
            {{ user.username }}
          </strong>
          {{ user.role }}
        </q-tooltip>
      </q-avatar>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useProjectStore } from 'src/stores/project';
import { useRoute } from 'vue-router';
import { useQuasar } from 'quasar';
const $q = useQuasar();

const store = useProjectStore();
const users = computed(() => store.projectUsers);
const loading = ref(false);
const error = ref(null);
const numberOfUsersToShow = ref(5);
const route = useRoute();

const fetchProjectUsers = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.fetchProjectUsers(route.params.id);
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
// route.params.id
const deleteProjectUser = async (id) => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.deleteProjectUser({
      projectId: route.params.id,
      userId: id,
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

onMounted(async () => {
  await fetchProjectUsers();
});
</script>

<style lang="scss">
.overlapping {
  .q-badge {
    border-radius: 50%;
    opacity: 0;
    visibility: hidden;
    transition: 0.3s;
    cursor: pointer;
  }
  &:hover {
    .q-badge {
      opacity: 1;
      visibility: visible;
    }
  }
}
</style>
