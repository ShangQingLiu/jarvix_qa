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

          <div class="flex justify-end items-center full-width">
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              rounded
              to="/user-authentication-and-management/login"
              v-if="Object.keys(store.user).length === 0"
              >
              {{ $t(`MainLayout.loginBtn`)  }}
              </q-btn
            >
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              rounded
              @click="logout"
              v-if="Object.keys(store.user).length !== 0"
              >
              {{ $t(`MainLayout.logoutBtn`)  }}
              </q-btn
            >
            <div
              v-if="Object.keys(store.user).length !== 0"
              class="gt-md flex flex-center"
            >
              <q-item class="user-profile q-py-none">
                <q-item-section avatar>
                  <q-avatar size="60px">
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
                  </q-avatar>
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-dark">
                    {{ store.user.username }}
                  </q-item-label>
                  <q-item-label caption>{{ store.user.email }}</q-item-label>
                  <q-item-label class="text-dark">
                    {{ store.user.role }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </div>
            <q-select
              v-model="locale"
              :options="localeOptions"
              bg-color="white"
              text-color="dark"
              emit-value
              map-options
              filled
              style="min-width: 160px"
            />
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer v-model="leftDrawerOpen" class="left-sidebar" show-if-above :width="350">
        <div class="logo-container q-my-xl text-center">
          <img style="max-width: 200px" src="/static/logo.svg" />
        </div>
        <q-list class="">
          <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" />
        </q-list>
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useI18n } from 'vue-i18n';
// Title here are translation files keys
const linksList = [
  {
    title: 'UserAuthenticationAndManagement',
    icon: 'img:/static/user-management.svg',
    link: '/user-authentication-and-management',
  },
  {
    title: 'Index',
    icon: 'img:/static/project-management.svg',
    link: '/',
  },
  {
    title: 'FileManagement',
    icon: 'img:/static/file-management.svg',
    link: '/file-management',
  },
  {
    title: 'Services',
    icon: 'img:/static/index-preparation.svg',
    link: '/index-preparation',
  },
];
export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);
    const search = ref('');
    const router = useRouter();
    const store = useAuthStore();
    const { locale } = useI18n({ useScope: 'global' });

    function logout() {
      localStorage.removeItem('jarvixUser');
      store.user = {};
      router.push('user-authentication-and-management/login');
    }
    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      search,
      logout,
      store,
      locale,
      localeOptions: [
        { value: 'en-US', label: 'English' },
        { value: 'zhHans', label: 'Chineese ( Simplified )' },
        { value: 'zhHant', label: 'Chineese ( Traditional )' },
      ],
    };
  },
});
</script>

<style lang="scss">
.q-drawer--left {
  // border-radius: 0px 20px 20px 0px;
  background: linear-gradient(90deg, #005055 0%, #006464 99.99%);
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
