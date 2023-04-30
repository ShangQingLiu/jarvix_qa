<template>
  <div class="q-pa-md">
    <q-layout class="q-pa-md" view="lHh Lpr lFf">
      <q-header class="bg-transparent q-pa-md">
        <q-toolbar>
          <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            @click="toggleLeftDrawer"
            class="lt-md"
          />
          <div class="row full-width">
            <div class="col-xs-12 col-md-9">
              <q-input
                rounded
                bg-color="white"
                standout="bg-white text-dark"
                class="elevation-0 q-mr-md full-width"
                v-model="search"
                placeholder="Search"
                :input-style="{ color: '#878787' }"
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="dark-page" />
                </template>
              </q-input>
            </div>
            <div class="gt-md col-xs-12 col-md-3 q-py-none flex flex-center">
              <q-item class="user-profile q-py-none">
                <q-item-section top avatar>
                  <q-avatar size="60px">
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
                  </q-avatar>
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-dark">Randy Riley</q-item-label>
                  <q-item-label caption>randy.riley@gmail.com</q-item-label>
                </q-item-section>
              </q-item>
            </div>
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer v-model="leftDrawerOpen" show-if-above :width="350">
        <div class="logo-container q-my-xl text-center">
          <img style="max-width: 200px" src="../assets/logo.svg" />
        </div>
        <q-list class="q-ml-xl">
          <q-item-label header>Main Menu</q-item-label>

          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";

const linksList = [
  {
    title: "Project Management",
    icon: "img:src/assets/project-management.svg",
    link: "/",
  },
  {
    title: "User Authentication and User Management",
    icon: "img:src/assets/user-management.svg",
    link: "/user-authentication-and-management",
  },
  {
    title: "File Management",
    icon: "img:src/assets/file-management.svg",
    link: "/file-management",
  },
  {
    title: "Index Preparation",
    icon: "img:src/assets/index-preparation.svg",
    link: "/index-preparation",
  },
];

export default defineComponent({
  name: "MainLayout",

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);
    const search = ref("");
    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      search,
    };
  },
});
</script>

<style lang="scss">
.q-drawer--left {
  border-radius: 0px 20px 20px 0px;
}
.user-profile {
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
