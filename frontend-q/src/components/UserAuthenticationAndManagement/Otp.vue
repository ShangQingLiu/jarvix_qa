<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">Otp Code</div>
    <div v-if="loading" class="q-py-lg flex justify-center">
      <q-spinner color="dark" size="3em" />
    </div>
    <div v-if="error" class="q-py-sm flex justify-center">
      <div class="text-h6 text-negative">
        {{ error }}
      </div>
    </div>
    <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs">
      We have sent the code to
      <span class="text-dark"> jamesjacob@gmail.com </span>
    </div>
    <q-form @submit.prevent="submitOtpCode">
      <div class="row">
        <div class="col-12">
          <div style="display: flex; flex-direction: row">
            <v-otp-input
              ref="otpInput"
              v-model:value="bindModal"
              input-classes="otp-input"
              separator=" "
              :num-inputs="4"
              :should-auto-focus="true"
              input-type="letter-numeric"
              :conditionalClass="['one', 'two', 'three', 'four']"
              :placeholder="['', '', '', '']"
              @on-change="handleOnChange"
              @on-complete="handleOnComplete"
            />
          </div>
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
        to="/user-authentication-and-management/new-password"
        >Continue</q-btn
      >
      <div class="text-subtitle1 text-dark-page q-mt-md q-mb-xs">
        Didn’t receive the code
        <router-link
          to="/user-authentication-and-management/forgot-password"
          class="text-primary no-underline"
        >
          click to resend
        </router-link>
      </div>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from "src/stores/auth";
import { ref } from "vue";
import VOtpInput from "vue3-otp-input";

const username = ref("");
const password = ref("");

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const submitOtpCode = async () => {
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
    error.value = err.response.status + " - " + err.response.statusText;
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
const otpInput = ref(null);
const bindModal = ref("");

const handleOnComplete = (value) => {
  console.log("OTP completed: ", value);
};

const handleOnChange = (value) => {
  console.log("OTP changed: ", value);
};

const clearInput = () => {
  otpInput.value?.clearInput();
};

const fillInput = (value) => {
  console.log(value);
};
</script>

<style>
.otp-input {
  width: 60px;
  height: 60px;
  margin-right: 10px;
  text-align: center;
  border: 0px solid transparent;
  font-style: normal;
  font-weight: 400;
  font-size: 38px;
  line-height: 57px;
}
</style>
