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
        <q-breadcrumbs-el label="Set new pasword" />

        /></q-breadcrumbs
      >
    </div>
    <div class="col-6">
      <!-- Login -->
      <NewPassword />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import NewPassword from "src/components/UserAuthenticationAndManagement/NewPassword.vue";
</script>

<style lang="scss"></style>
