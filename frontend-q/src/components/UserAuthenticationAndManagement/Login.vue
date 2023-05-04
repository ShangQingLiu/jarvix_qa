<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">Login</div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner color="dark" size="3em" />
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
            placeholder="User name"
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
            placeholder="Password"
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
        >Login</q-btn
      >
      <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs">
        Don’t have a account?
        <router-link
          to="/user-authentication-and-management/register"
          class="text-primary no-underline"
        >
          Sign Up
        </router-link>
      </div>
      <div class="text-subtitle1 text-dark-page">
        If don’t remember your password,
        <router-link
          to="/user-authentication-and-management/forgot-password"
          class="text-primary no-underline"
        >
          Forget Password
        </router-link>
      </div>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from "src/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";
const username = ref("");
const password = ref("");
const router = useRouter();

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const loginUser = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.loginUser({
      username: username.value,
      password: password.value,
    });
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
    router.push("/user-authentication-and-management");
  }
};
</script>