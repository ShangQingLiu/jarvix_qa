<template>
  <div class="col-12">
    <q-card flat class="bg-white q-mb-lg">
      <q-card-section>
        <div class="text-h6 text-weight-bold text-dark">
          {{ $t('pages.IndexPage.Detail.ProjectUsers.title') }}
        </div>
        <q-separator class="q-my-lg" />
        <div v-if="loading" class="q-py-lg flex justify-center">
          <q-spinner-oval color="primary" size="2rem" />
        </div>
        <div v-if="error" class="q-py-sm flex justify-center">
          <div class="text-h6 text-negative">
            {{ error }}
          </div>
        </div>
        <q-list>
          <q-item
            v-for="(user, i) in users.slice(0, numberOfUsersToShow)"
            :key="i"
            class="q-py-none q-px-none list-item q-mb-lg"
          >
            <q-item-section>
              <q-item-label class="text-dark">
                {{ user.username }} ({{ user.role }})
              </q-item-label>
              <q-item-label caption>
                {{ user.email }}
              </q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-btn
                round
                color="negative"
                unelevated
                class="q-mx-xs"
                icon="delete"
                @click="deleteProjectUser(user.id)"
                size="sm"
              />
            </q-item-section>
          </q-item>
          <q-item v-if="users.length === 0">
            <q-item-section>
              {{ $t('pages.IndexPage.Detail.ProjectUsers.noFound') }}
            </q-item-section>
          </q-item>
        </q-list>
        <q-separator class="q-my-lg" />
        <q-item-label
          @click="numberOfUsersToShow = users.length"
          v-if="users.length >= 10 && numberOfUsersToShow !== users.length"
          header
          class="text-primary cursor-pointer q-pl-none"
        >
          {{ $t('pages.IndexPage.Detail.ProjectUsers.viewAll') }}
        </q-item-label>
        <q-item-label
          @click="numberOfUsersToShow = 10"
          v-if="numberOfUsersToShow == users.length"
          header
          class="text-primary cursor-pointer q-pl-none"
        >
          {{ $t('pages.IndexPage.Detail.ProjectUsers.viewLess') }}
        </q-item-label>
      </q-card-section>
    </q-card>
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

<style lang="scss"></style>
