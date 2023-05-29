<template>
  <div>
    <div class="row q-col-gutter-md">
      <div class="col-12">
        <q-card flat class="bg-transparent q-mb-lg">
          <q-card-section class="q-px-none">
            <div class="text-h6 text-weight-bold text-dark q-mb-md">
              {{ $t('pages.IndexPage.Invite.title') }}
            </div>
            <div v-if="loading" class="q-py-lg flex justify-center">
              <q-spinner-oval color="primary" size="3rem" />
            </div>
            <div v-if="error" class="q-py-sm flex justify-center">
              <div class="text-h6 text-negative">
                {{ error }}
              </div>
            </div>
            <q-form @submit.prevent="sendProjectInvitation">
              <div class="row">
                <div class="col-12 col-md-8 q-mb-md">
                  <q-select
                    v-model="locale"
                    :options="localeOptions"
                    outlined
                    text-color="dark"
                    bg-color="white"
                    emit-value
                    map-options
                    dense
                  >
                    <template v-slot:selected>
                      {{ $t(`MainLayout.languages.${selectedLabel(locale)}`) }}
                    </template>
                    <template v-slot:option="scope">
                      <q-item v-bind="scope.itemProps">
                        <q-item-section>
                          <q-item-label>
                            {{
                              $t(`MainLayout.languages.${scope.opt.label}`)
                            }}</q-item-label
                          >
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>
              </div>
              <div class="row">
                <div class="col-12">
                  <div
                    class="row q-col-gutter-md"
                    v-for="(content, i) in inviteContent"
                    :key="i"
                  >
                    <div class="col-8 col-md-6">
                      <q-input
                        v-model="content.email"
                        :placeholder="$t('pages.IndexPage.Invite.email')"
                        class="q-mb-md"
                        type="email"
                        borderless
                        bg-color="white"
                        :input-style="{ padding: '0px 23px' }"
                        dense
                        required
                      />
                    </div>
                    <div class="col-4 col-md-2">
                      <q-select
                        v-model="content.role"
                        :options="content.roleOptions"
                        outlined
                        text-color="dark"
                        bg-color="white"
                        emit-value
                        map-options
                        dense
                        borderless
                      >
                        <template v-slot:selected>
                          {{
                            !content.role ? '' : $t(`MainLayout.roles.${content.role}`)
                          }}
                        </template>
                        <template v-slot:option="scope">
                          <q-item v-bind="scope.itemProps">
                            <q-item-section>
                              <q-item-label>
                                {{ $t(`MainLayout.roles.${scope.opt}`) }}</q-item-label
                              >
                            </q-item-section>
                          </q-item>
                        </template>
                      </q-select>
                    </div>
                  </div>
                </div>
                <div class="col-12 q-pt-none q-mb-md" @click="pushField">
                  <q-btn
                    color="dark1"
                    text-color="dark1"
                    unelevated
                    class="bg-transparent text-capitalize"
                  >
                    {{ $t('pages.IndexPage.Invite.addField') }}
                  </q-btn>
                </div>
                <div class="col-12">
                  <q-btn
                    color="primary"
                    unelevated
                    class="text-dark text-capitalize"
                    type="submit"
                  >
                    {{ $t('pages.IndexPage.Invite.inviteBtn') }}
                  </q-btn>
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';

import { useRoute, useRouter } from 'vue-router';
import { useProjectStore } from 'src/stores/project';

// inside of a Vue file
import { useQuasar } from 'quasar';
const store = useProjectStore();
const route = useRoute();
const router = useRouter();
const inviteEmail = ref('');
const loading = ref(false);
const error = ref(null);
const $q = useQuasar();

// const serviceStore = useServiceStore();
const locale = ref('EN');
const localeOptions = ref([
  { value: 'EN', label: 'english' },
  { value: 'ZH-CN', label: 'chineeseSimplified' },
  { value: 'ZH-TW', label: 'chineeseTraditional' },
]);
const inviteContent = reactive([
  {
    email: '',
    role: 'user',
    roleOptions: ['user', 'admin'],
  },
]);
const pushField = () => {
  inviteContent.push({
    email: '',
    role: 'user',
    roleOptions: ['user', 'admin'],
  });
};
const selectedLabel = (item) => {
  const option = localeOptions.value.find((i) => i.value == item);
  return option.label;
};
const sendProjectInvitation = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.invitePeople({
      inviteContent: inviteContent,
      projectId: route.params.id,
      language: locale.value,
    });
    if (res) {
      $q.notify({
        message: 'Successful send the invitation.',
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
const currentProject = computed(() => {
  return store.userProjects.find((project) => project.id == route.params.id);
});
onMounted(() => {
  console.log(currentProject.value);

  if (!currentProject.value) {
    router.push('/');
  }
});
</script>

<style lang="scss"></style>
