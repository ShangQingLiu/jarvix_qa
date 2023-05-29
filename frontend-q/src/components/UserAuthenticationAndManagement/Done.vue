<template>
  <div>
    <div class="text-h6 text-weight-bold text-dark q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.DonePage.Done.title') }}
      !!
    </div>

    <div class="text-subtitle1 text-dark-page q-mt-md q-mb-md">
      {{ $t('pages.UserAuthenticationAndManagement.DonePage.Done.subtitle') }}
    </div>
    <q-btn
      color="primary"
      unelevated
      class="text-capitalize"
      text-color="white"
      square
      style="width: 200px"
      to="/auth/login"
    >
      {{ $t('pages.UserAuthenticationAndManagement.DonePage.Done.loginBtn') }}
    </q-btn>
  </div>
</template>
<script setup></script>
