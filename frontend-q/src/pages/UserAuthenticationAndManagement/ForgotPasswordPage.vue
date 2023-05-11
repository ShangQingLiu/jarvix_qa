<template>
  <div class="row">
    <div class="col-12">
      <!-- BreadCrumbs -->
      <q-breadcrumbs
        separator-color="dark-page"
        class="text-dark q-mb-md"
        active-color="dark-page"
      >
        <template v-slot:separator>
          <q-icon size="1.5em" name="chevron_right" color="dark-page" />
        </template>

        <q-breadcrumbs-el
          label="User Authentication and User Management"
          to="/user-authentication-and-management"
        />
        <q-breadcrumbs-el label="Forget Password" />

        /></q-breadcrumbs
      >
    </div>
    <div class="col-6">
      <!-- Login -->
      <ForgotPassword />
    </div>
  </div>
</template>

<script setup>
import ForgotPassword from "src/components/UserAuthenticationAndManagement/ForgotPassword.vue";
</script>

<style lang="scss"></style>
