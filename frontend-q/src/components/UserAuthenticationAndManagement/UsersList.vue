<template>
  <div class="col-12">
    <q-card flat class="bg-white q-mb-lg">
      <q-card-section>
        <div class="text-h6 text-weight-bold text-dark">
          {{ $t('pages.UserAuthenticationAndManagement.IndexPage.UsersList.title') }}
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
            <q-item-section avatar>
              <q-avatar size="45px">
                <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-dark">
                {{ user.username }} ({{ user.role }})
              </q-item-label>
              <q-item-label caption>
                {{ user.email }}
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
                  @click="
                    $router.push(`/user-authentication-and-management/view/${user.id}`)
                  "
                  size="sm"
                />
                <q-btn
                  round
                  color="primary"
                  unelevated
                  class="q-mx-xs"
                  icon="edit"
                  v-if="store.user.id === user.id"
                  @click="
                    $router.push(`/user-authentication-and-management/edit/${user.id}`)
                  "
                  size="sm"
                />
                <q-btn
                  round
                  color="negative"
                  unelevated
                  class="q-mx-xs"
                  icon="delete"
                  @click="deleteUser(user.id)"
                  v-if="store.user.id === user.id"
                  size="sm"
                />
              </div>
            </q-item-section>
          </q-item>
          <q-item v-if="users.length === 0">
            <q-item-section>
              {{
                $t('pages.UserAuthenticationAndManagement.IndexPage.UsersList.noFound')
              }}
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
          {{ $t('pages.UserAuthenticationAndManagement.IndexPage.UsersList.viewAll') }}
        </q-item-label>
        <q-item-label
          @click="numberOfUsersToShow = 10"
          v-if="numberOfUsersToShow == users.length"
          header
          class="text-primary cursor-pointer q-pl-none"
        >
          {{ $t('pages.UserAuthenticationAndManagement.IndexPage.UsersList.viewLess') }}
        </q-item-label>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';
const store = useAuthStore();
const users = computed(() => store.usersList);
const loading = ref(false);
const error = ref(null);
const numberOfUsersToShow = ref(10);

const fetchUsers = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.fetchUsers();
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const deleteUser = async (id) => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.deleteUser(id);
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchUsers();
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
