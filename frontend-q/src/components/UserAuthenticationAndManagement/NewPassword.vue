<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.NewPasswordPage.NewPassword.title') }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
     <q-spinner-oval color="primary" size="2rem" />
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
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            v-model="password"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.NewPasswordPage.NewPassword.form.password'
              )
            "
            class="q-mb-md"
            type="password"
          />
          <q-input
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            v-model="confirmPassword"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.NewPasswordPage.NewPassword.form.confirmPassword'
              )
            "
            class="q-mb-md"
            type="password"
          />
        </div>
      </div>

      <q-btn
        color="primary"
        unelevated
        class="text-capitalize q-mt-xl"
        text-color="white"
        to="/user-authentication-and-management/done"
        square
        style="width: 200px"
      >
        {{
          $t('pages.UserAuthenticationAndManagement.NewPasswordPage.NewPassword.form.btn')
        }}
      </q-btn>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from 'src/stores/auth';
import { ref } from 'vue';

const username = ref('');
const password = ref('');

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const loginUser = async () => {
  try {
    error.value = null;
    loading.value = true;
    // const res = await store.loginUser({
    //   username: username.value,
    //   password: password.value,
    // });
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
