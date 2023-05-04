<template>
  <div>
    <div class="row q-col-gutter-md">
      <div class="col-12">
        <q-card flat class="bg-white q-mb-lg">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">Invite People</div>
            <q-separator class="q-my-lg" />
            <div v-if="loading" class="q-py-lg flex justify-center">
              <q-spinner color="dark" size="3em" />
            </div>
            <div v-if="error" class="q-py-sm flex justify-center">
              <div class="text-h6 text-negative">
                {{ error }}
              </div>
            </div>
            <q-form @submit.prevent="sendProjectInvitation">
              <div class="row q-col-gutter-md">
                <div class="col-10">
                  <q-input
                    v-model="inviteEmail"
                    placeholder="Email"
                    class="q-mb-md"
                    type="email"
                    bg-color="accent"
                    :input-style="{ padding: '0px 23px' }"
                    borderless
                    dense
                    required
                  />
                </div>
                <div class="col-2">
                  <q-btn
                    color="primary"
                    unelevated
                    class="text-dark text-capitalize full-width"
                    text-color="white"
                    type="submit"
                    >Invite</q-btn
                  >
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
import { ref, computed, onMounted } from "vue";

import { useRoute, useRouter } from "vue-router";
import { useProjectStore } from "src/stores/project";
// inside of a Vue file
import { useQuasar } from "quasar";
const store = useProjectStore();
const route = useRoute();
const router = useRouter();
const inviteEmail = ref("");
const loading = ref(false);
const error = ref(null);
const $q = useQuasar();
const sendProjectInvitation = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.sendProjectInvitation({
      email: inviteEmail.value,
      projectId: route.params.id,
    });
    if (res) {
      $q.notify({
        message: res.message,
        position: "top-right",
        color: "primary",
      });
      router.push("/");
    }
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
  } finally {
    loading.value = false;
  }
};
const currentProject = computed(() => {
  return store.projectsList.find((project) => project.id == route.params.id);
});
onMounted(() => {
  if (!currentProject.value) {
    router.push("/");
  }
});
</script>

<style lang="scss"></style>