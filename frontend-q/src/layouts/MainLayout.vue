<template>
  <div class="">
    <q-layout class="q-pa-md" view="lHh Lpr lFf">
      <q-header class="md-bg-primary q-px-none q-px-md-sm q-py-lg q-py-md-sm">
        <q-toolbar>
          <div class="flex justify-between items-center full-width">
            <q-btn
              flat
              dense
              round
              icon="menu"
              aria-label="Menu"
              @click="toggleLeftDrawer"
              class="lt-md"
            />
            <div class="logo-container lt-md text-center">
              <img style="max-width: 150px" src="/static/logo.svg" />
            </div>

            <!-- Desktop -->
            <div class="flex justify-between items-center full-width gt-sm">
              <q-btn
                color="primary"
                unelevated
                class="text-capitalize"
                text-color="white"
                rounded
                to="/auth/login"
                v-if="Object.keys(store.user).length === 0"
              >
                {{ $t(`MainLayout.loginBtn`) }}
              </q-btn>
              <div class="flex">
                <q-item
                  class="q-mr-md"
                  clickable
                  to="/user-authentication-and-management"
                >
                  <q-item-section>
                    <q-item-label class="text-dark2">{{
                      $t(`MainLayout.links.UserAuthenticationAndManagement`)
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
                <q-item class="q-mr-md" clickable to="/">
                  <q-item-section>
                    <q-item-label class="text-dark2">{{
                      $t(`MainLayout.links.Index`)
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
              </div>
              <div class="flex items-center">
                <div
                  v-if="Object.keys(store.user).length !== 0"
                  class="flex flex-center gt-sm"
                >
                  <q-btn-dropdown no-caps dropdown-icon="expand_more" text-color="white">
                    <template v-slot:label>
                      <div class="row items-center no-wrap">
                        <div class="column">
                          <q-avatar size="50px">
                            <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
                          </q-avatar>
                        </div>
                        <div class="q-mx-sm" />
                        <div class="column">
                          <q-item-label class="text-white text-left text-weight-regular">
                            {{ store.user.username }}
                          </q-item-label>
                          <q-item-label caption class="text-white">{{ store.user.email }}</q-item-label>
                        </div>
                      </div>
                    </template>

                    <div class="row no-wrap q-pa-md">
                      <div class="column">
                        <q-item-section>
                          <q-item-label class="text-weight-regular">
                            {{ store.user.role }}
                          </q-item-label>
                        </q-item-section>
                      </div>

                      <q-separator vertical inset class="q-mx-lg" />
                      <div class="column items-center">
                        <q-btn
                          color="primary"
                          unelevated
                          class="text-capitalize"
                          text-color="white"
                          rounded
                          @click="logout"
                          v-if="Object.keys(store.user).length !== 0"
                        >
                          {{ $t(`MainLayout.logoutBtn`) }}
                        </q-btn>
                      </div>
                    </div>
                  </q-btn-dropdown>
                </div>
                <q-select
                  v-model="locale"
                  :options="localeOptions"
                  outlined
                  text-color="white"
                  emit-value
                  map-options
                  style="min-width: 160px"
                  dense
                  class="language-dropdown white-language-dropdown gt-sm"
                >
                  <template v-slot:selected>
                    {{ $t(`MainLayout.languages.${selectedLabel(locale)}`) }}
                  </template>
                  <template v-slot:option="scope">
                    <q-item v-bind="scope.itemProps">
                      <q-item-section>
                        <q-item-label>
                          {{
                            $t(`MainLayout.languages.${scope.opt.label}`)
                          }}</q-item-label
                        >
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>
              </div>
            </div>
            <!-- Mobile -->
            <div class="flex justify-end items-center lt-md">
              <div
                v-if="Object.keys(store.user).length !== 0"
                class="flex flex-center lt-md"
              >
                <q-btn-dropdown no-caps dropdown-icon="expand_more">
                  <template v-slot:label>
                    <div class="row items-center no-wrap">
                      <q-avatar size="30px">
                        <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
                      </q-avatar>
                    </div>
                  </template>

                  <div class="row no-wrap q-pa-md">
                    <div class="column">
                      <q-item-section>
                        <q-item-label class="text-weight-regular">
                          {{ store.user.username }}
                        </q-item-label>
                        <q-item-label caption class="">{{ store.user.email }}</q-item-label>
                        <q-item-label class="text-weight-regular">
                          {{ store.user.role }}
                        </q-item-label>
                      </q-item-section>
                    </div>

                    <q-separator vertical inset class="q-mx-lg" />

                    <div class="column items-center">
                      <q-btn
                        color="primary"
                        unelevated
                        class="text-capitalize"
                        text-color="white"
                        rounded
                        @click="logout"
                        v-if="Object.keys(store.user).length !== 0"
                      >
                        {{ $t(`MainLayout.logoutBtn`) }}
                      </q-btn>
                    </div>
                  </div>
                </q-btn-dropdown>
              </div>
            </div>
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer v-model="leftDrawerOpen" class="left-sidebar" show-if-above :width="350">
        <div class="logo-container q-my-xl text-center">
          <img style="max-width: 200px" src="/static/logo.svg" />
        </div>
        <!-- Desktop -->
        <q-list class="q-ml-lg gt-sm">
          <!-- <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" /> -->
          <q-item class="q-mb-md" clickable to="/file-management">
            <q-item-section avatar>
              <q-icon size="30px" name="img:/static/file-management.svg" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-dark2">{{
                $t(`MainLayout.links.FileManagement`)
              }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item class="q-mb-md" clickable to="/index-preparation">
            <q-item-section avatar>
              <q-icon size="30px" name="img:/static/index-preparation.svg" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-dark2">{{
                $t(`MainLayout.links.Services`)
              }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-list class="q-ml-lg lt-md">
          <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" />
        </q-list>
      </q-drawer>

      <q-page-container>
        <div class="flex justify-between items-center full-width lt-md q-mb-md">
          <q-select
            v-model="locale"
            :options="localeOptions"
            outlined
            text-color="dark"
            emit-value
            map-options
            style="max-width: 160px"
            dense
            class="language-dropdown"
            color="white"
            icon-color="white"
          >
            <template v-slot:selected>
              {{ $t(`MainLayout.languages.${selectedLabel(locale)}`) }}
            </template>
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section>
                  <q-item-label>
                    {{ $t(`MainLayout.languages.${scope.opt.label}`) }}</q-item-label
                  >
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>

        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useServiceStore } from 'src/stores/service';
import { useProjectStore } from 'src/stores/project';

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
    const serviceStore = useServiceStore();
    const projectStore = useProjectStore();

    const { locale } = useI18n({ useScope: 'global' });

    function logout() {
      localStorage.removeItem('jarvixUser');
      localStorage.setItem('currentSelectedProject', projectStore.selectedProject);
      store.user = {};
      serviceStore.chatHistory = [];
      router.push('/auth/login');
    }
    watch(locale, (val) => {
      if (val == 'en-US') {
        serviceStore.currentLanguage = 'EN';
      } else if (val == 'zhHans') {
        serviceStore.currentLanguage = 'ZH_CN';
      } else {
        serviceStore.currentLanguage = 'ZH_TW';
      }
    });
    const localeOptions = ref([
      { value: 'en-US', label: 'english' },
      { value: 'zhHans', label: 'chineeseSimplified' },
      { value: 'zhHant', label: 'chineeseTraditional' },
    ]);
    const selectedLabel = (item) => {
      const option = localeOptions.value.find((i) => i.value == item);
      return option.label;
    };

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
      localeOptions,
      selectedLabel,
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
    font-weight: 500;
    font-size: 17px;
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
.language-dropdown {
  border: 0.5px solid #878787;
  .q-field--auto-height.q-field--dense .q-field__control {
    height: 30px;
  }
  .q-field__native {
    font-weight: 400 !important;
    font-size: 12px !important;
    line-height: 16px !important;
    color: #000 !important;
    span {
      font-weight: 400 !important;
      font-size: 12px !important;
      line-height: 16px !important;
      color: #000 !important;
    }
  }
  .q-select__dropdown-icon {
    color: #000;
  }
}

.white-language-dropdown {
  border: 0.5px solid #fff;
  .q-field__native {
    color: #fff !important;
    span {
      color: #fff !important;
    }
  }
  .q-select__dropdown-icon {
    color: #fff;
  }
}

.q-header .q-field__control {
  height: 30px;
}
.q-router-link--active {
  border-bottom: 3px solid $primary;
  .q-item__label {
    color: #fff !important;
  }
}
</style>
