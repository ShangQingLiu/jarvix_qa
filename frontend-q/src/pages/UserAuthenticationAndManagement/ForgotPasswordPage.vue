<template>
  <div class="row justify-center">
    <div class="col-12">
      <!-- BreadCrumbs -->
      <!-- <q-breadcrumbs
        separator-color="dark-page"
        class="text-dark q-mb-md"
        active-color="dark-page"
      >
        <template v-slot:separator>
          <q-icon size="1.5em" name="chevron_right" color="dark-page" />
        </template>

        <q-breadcrumbs-el
          :label="
            $t(
              'pages.UserAuthenticationAndManagement.ForgotPasswordPage.breadcrumbs.label'
            )
          "
          to="/user-authentication-and-management"
        />
        <q-breadcrumbs-el
          :label="
            $t(
              'pages.UserAuthenticationAndManagement.ForgotPasswordPage.breadcrumbs.label2'
            )
          "
        />

        /></q-breadcrumbs
      > -->
    </div>
    <div class="col-12 col-md-9">
      <!-- Login -->
      <ForgotPassword />
    </div>
  </div>
</template>

<script setup>
import ForgotPassword from 'src/components/UserAuthenticationAndManagement/ForgotPassword.vue';
</script>

<style lang="scss"></style>
