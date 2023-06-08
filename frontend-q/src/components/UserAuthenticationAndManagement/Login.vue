<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.LoginPage.Login.title') }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner-oval color="primary" size="3rem" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <q-form @submit.prevent="loginUser">
      <div class="row">
        <div class="col-12">
          <q-input
            v-model="username"
            :placeholder="
              $t('pages.UserAuthenticationAndManagement.LoginPage.Login.form.username')
            "
            class="q-mb-md"
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
          />

          <q-input
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            v-model="password"
            :placeholder="
              $t('pages.UserAuthenticationAndManagement.LoginPage.Login.form.password')
            "
            class="q-mb-md"
            type="password"
          />
        </div>
      </div>
      <q-btn
        color="primary"
        unelevated
        class="text-capitalize q-mt-xl md-block q-mx-auto q-mx-md-none"
        text-color="white"
        type="submit"
        square
        style="width: 200px"
      >
        {{ $t('pages.UserAuthenticationAndManagement.LoginPage.Login.form.btn') }}
      </q-btn>
      <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs text-md-center">
        {{
          $t('pages.UserAuthenticationAndManagement.LoginPage.Login.form.dontAccountText')
        }}
        <router-link to="/auth/register" class="text-primary no-underline">
          {{ $t('pages.UserAuthenticationAndManagement.LoginPage.Login.form.signupBtn') }}
        </router-link>
      </div>
      <div class="text-subtitle1 text-dark-page text-md-center">
        {{
          $t(
            'pages.UserAuthenticationAndManagement.LoginPage.Login.form.dontRememberText'
          )
        }},
        <router-link to="/auth/forgot-password" class="text-primary no-underline">
          {{
            $t(
              'pages.UserAuthenticationAndManagement.LoginPage.Login.form.forgotPasswordBtn'
            )
          }}
        </router-link>
      </div>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from 'src/stores/auth';
import { useProjectStore } from 'src/stores/project';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';

const username = ref('');
const password = ref('');
const router = useRouter();
const $q = useQuasar();

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const projectStore = useProjectStore();

const fetchUserProjects = async (id) => {
  try {
    error.value = null;
    loading.value = true;

    const res = await projectStore.fetchUserProjects(id);
    const indexedProjects = await projectStore.getIndexedProjects();
    const filteredProjects = res.filter((project, index) => {
      if (indexedProjects[index].message === 'Index exists') {
        return project;
      }
    });
    // If project exists
    if (filteredProjects.length > 1) {
      const savedProject = localStorage.getItem('currentSelectedProject');
      savedProject
        ? (projectStore.selectedProject = savedProject)
        : (projectStore.selectedProject = filteredProjects[0]);
      router.push('/index-preparation');
    } else {
      router.push('/');
      $q.notify({
        message: 'Please create new project and upload the file to use the service.',
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
const loginUser = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.loginUser({
      username: username.value,
      password: password.value,
    });
    if (res) {
      const user = await store.getLoggedInUserData();
      if (user) {
        await fetchUserProjects(user.id);
      }
    }
  } catch (err) {
    console.log(err);
    error.value = 'Invalid user name or password, please try again.';
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
