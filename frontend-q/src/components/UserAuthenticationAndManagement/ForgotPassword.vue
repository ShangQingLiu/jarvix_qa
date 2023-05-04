<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      Forgot Password
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner color="dark" size="3em" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <q-form @submit.prevent="getCode">
      <div class="row">
        <div class="col-12">
          <q-input
            v-model="email"
            placeholder="Email"
            class="q-mb-md"
            borderless
            type="email"
            bg-color="white"
            :input-style="{ padding: '0px 23px' }"
          />
        </div>
      </div>

      <div class="row q-gutter-md q-mt-sm">
        <q-btn
          color="white"
          unelevated
          class="text-capitalize"
          text-color="dark"
          square
          style="width: 200px"
          to="/user-authentication-and-management/login"
          >Go back to login</q-btn
        >
        <!-- <q-btn
          color="primary"
          unelevated
          class="text-capitalize"
          text-color="white"
          type="submit"
          square
          style="width: 200px"
          to="/UserAuthenticationAndManagement/otp-code"
          >Send code</q-btn
        > -->
        <q-btn
          color="primary"
          unelevated
          class="text-capitalize"
          text-color="white"
          square
          style="width: 200px"
          to="/user-authentication-and-management/otp-code"
          >Send code</q-btn
        >
      </div>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from "src/stores/auth";
import { ref } from "vue";

const email = ref("");

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const getCode = async () => {
  try {
    error.value = null;
    loading.value = true;
    // const res = await store.getCode({

    //   email: email.value,

    // });
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
