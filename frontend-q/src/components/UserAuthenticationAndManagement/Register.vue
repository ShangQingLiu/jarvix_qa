<template>
  <div>
    <div class="text-h6 text-dark q-mb-md text-weight-light">
      {{ $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.title') }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner-oval color="primary" size="3rem" />
    </div>

    <div v-if="error" class="q-py-sm flex">
      <div class="text-body1 text-negative">! {{ error }}</div>
    </div>
    <q-form @submit.prevent="registerUser">
      <div class="row">
        <div class="col-12">
          <q-input
            v-model="username"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.username'
              )
            "
            class="q-mb-md"
            outlined
            bg-color="transparent"
            :input-style="{ padding: '0px 23px' }"
          />
          <q-input
            v-model="email"
            :placeholder="
              $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.form.email')
            "
            type="email"
            class="q-mb-md"
            outlined
            bg-color="transparent"
            :input-style="{ padding: '0px 23px' }"
          />

          <q-input
            v-model="password"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.password'
              )
            "
            type="password"
            class="q-mb-md"
            outlined
            bg-color="transparent"
            :input-style="{ padding: '0px 23px' }"
          />
        </div>
      </div>
      <q-btn
        style="width: 188px"
        color="primary"
        unelevated
        class="text-capitalize q-my-lg md-block q-mx-auto q-mx-md-none"
        text-color="white"
        type="submit"
        rounded
      >
        {{ $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.form.btn') }}
      </q-btn>
      <!-- <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs">
        {{
          $t(
            'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.alreadyBtn'
          )
        }}
        <router-link to="/auth/login" class="text-primary no-underline">
          {{
            $t(
              'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.loginBtn'
            )
          }}
        </router-link>
      </div> -->
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from 'src/stores/auth';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const registerUser = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.registerUser({
      username: username.value,
      email: email.value,
      password: password.value,
    });
    console.log(res);
    if (res) {
      router.push('/auth/login');
    }
  } catch (err) {
    console.log(err);
    error.value = 'Please check the registration information and try to sign up again.';
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
