<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.title') }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
     <q-spinner-oval color="primary" size="3rem" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
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
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
          />
          <q-input
            v-model="email"
            :placeholder="
              $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.form.email')
            "
            class="q-mb-md"
            borderless
            type="email"
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
          />

          <q-input
            borderless
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
            v-model="password"
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.password'
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
        type="submit"
        square
        style="width: 200px"
      >
        {{ $t('pages.UserAuthenticationAndManagement.RegisterPage.Register.form.btn') }}
      </q-btn>
      <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs">
        {{
          $t(
            'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.alreadyBtn'
          )
        }}
        <router-link
          to="/auth/login"
          class="text-primary no-underline"
        >
          {{
            $t(
              'pages.UserAuthenticationAndManagement.RegisterPage.Register.form.loginBtn'
            )
          }}
        </router-link>
      </div>
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
