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
          :label="
            $t('pages.UserAuthenticationAndManagement.RegisterPage.breadcrumbs.label')
          "
          to="/user-authentication-and-management"
        />
        <q-breadcrumbs-el
          :label="
            $t('pages.UserAuthenticationAndManagement.RegisterPage.breadcrumbs.label2')
          "
        />

        /></q-breadcrumbs
      >
    </div>
    <div class="col-6">
      <!-- Register User -->
      <Register />
    </div>
  </div>
</template>

<script setup>
import Register from 'src/components/UserAuthenticationAndManagement/Register.vue';
</script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}
.list-item {
  .q-item__label {
    font-style: normal;
    font-weight: 600;
    font-size: 19px;
    line-height: 19px;
  }
  .q-item__label--caption {
    font-style: normal;
    font-weight: 400;
    font-size: 17px;
    line-height: 21px;
    color: $dark-page;
  }
}
</style>
