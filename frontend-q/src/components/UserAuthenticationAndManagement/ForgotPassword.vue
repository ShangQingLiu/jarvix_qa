<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{
        $t(
          'pages.UserAuthenticationAndManagement.ForgotPasswordPage.ForgotPassword.title'
        )
      }}
    </div>
    <div v-if="loading" class="q-py-lg flex justify-center">
     <q-spinner-oval color="primary" size="3rem" />
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
            :placeholder="
              $t(
                'pages.UserAuthenticationAndManagement.ForgotPasswordPage.ForgotPassword.form.email'
              )
            "
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
          class="text-capitalize md-block q-mx-auto q-mx-md-none"
          text-color="dark"
          square
          style="width: 200px"
          to="/user-authentication-and-management/login"
        >
          {{
            $t(
              'pages.UserAuthenticationAndManagement.ForgotPasswordPage.ForgotPassword.form.btn'
            )
          }}
        </q-btn>
        <q-btn
          color="primary"
          unelevated
          class="text-capitalize md-block q-mx-auto q-mx-md-none"
          text-color="white"
          square
          style="width: 200px"
          type="submit"
        >
          {{
            $t(
              'pages.UserAuthenticationAndManagement.ForgotPasswordPage.ForgotPassword.form.btn2'
            )
          }}
        </q-btn>
      </div>
    </q-form>
  </div>
</template>
<script setup>
import { useAuthStore } from 'src/stores/auth';
import { ref } from 'vue';
import { useQuasar } from 'quasar';

const email = ref('');
const $q = useQuasar();

const loading = ref(false);
const error = ref(null);
const store = useAuthStore();
const getCode = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.getCode({
      email: email.value,
    });
    console.log(res);
    if (res) {
      $q.notify({
        message: res.message,
        position: 'top-right',
        color: 'primary',
      });
    }
  } catch (err) {
    console.log(err);
    error.value =
      'Could not find any account belong to this email, please check the e-mail address and try again.';
    // console.log(err.response.statusText);
  } finally {
    loading.value = false;
  }
};
</script>
