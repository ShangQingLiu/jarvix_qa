<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.EditUserPage.EditUser.title') }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner-oval color="primary" size="3rem" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <q-form @submit.prevent="editUser">
      <div class="row">
        <div class="col-12">
          <q-input
            v-model="username"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.EditUserPage.EditUser.form.username'
              )
            "
            class="q-mb-md"
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            required
          />
          <q-input
            v-model="email"
            :placeholder="
              $t('pages.UserAuthenticationAndManagement.EditUserPage.EditUser.form.email')
            "
            class="q-mb-md"
            borderless
            type="email"
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            required
          />

          <q-input
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            v-model="password"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.EditUserPage.EditUser.form.password'
              )
            "
            class="q-mb-md"
            type="password"
            required
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
        {{ $t('pages.UserAuthenticationAndManagement.EditUserPage.EditUser.form.btn') }}
      </q-btn>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from 'src/stores/auth';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
const $q = useQuasar();
const route = useRoute();
const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const editUser = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.editUser({
      form: {
        username: username.value,
        email: email.value,
        password: password.value,
      },
      userId: route.params.id,
    });
    if (res) {
      $q.notify({
        message: 'User Updated successfully',
        position: 'top-right',
        color: 'primary',
      });
      router.push('/user-authentication-and-management');
    }
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
