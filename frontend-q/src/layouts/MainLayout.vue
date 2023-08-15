<template>
  <div class="">
    <q-layout class="q-pa-md" view="hHh lpR lFf">
      <q-header class="bg-white q-px-none q-px-md-sm q-py-lg q-py-md-sm">
        <q-toolbar>
          <div class="flex no-wrap items-center full-width">
            <div @click="$router.push('/')" class="logo-container lt-md text-center">
              <img style="max-width: 150px" src="/static/logo.svg" />
            </div>
            <div
              @click="$router.push('/')"
              class="logo-container gt-sm q-my-lg text-center flex justify-center"
              style="flex: 0 0 350px"
            >
              <img style="max-width: 200px" src="/static/logo.svg" />
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
              <!-- <div class="flex">
                <q-item
                  class="q-mr-md"
                  clickable
                  to="/user-authentication-and-management"
                >
                  <q-item-section>
                    <q-item-label class="text-dark">{{
                      $t(`MainLayout.links.UserAuthenticationAndManagement`)
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
                <q-item class="q-mr-md" clickable to="/">
                  <q-item-section>
                    <q-item-label class="text-dark">{{
                      $t(`MainLayout.links.Index`)
                    }}</q-item-label>
                  </q-item-section>
                </q-item>
              </div> -->
              <div class="flex items-center">
                <p class="text-dark q-mb-none">Project Name:</p>
                <q-select
                  v-model="projectName"
                  :placeholder="$t('pages.FileManagementPage.projectName')"
                  class="language-dropdown q-ml-md"
                  :options="userProjects"
                  option-value="name"
                  option-label="name"
                  emit-value
                  outlined
                  dense
                  style="min-width: 150px"
                />
              </div>
              <div class="flex items-center">
                <div
                  v-if="Object.keys(store.user).length !== 0"
                  class="flex flex-center gt-sm"
                >
                  <q-btn-dropdown no-caps dropdown-icon="expand_more" text-color="dark">
                    <template v-slot:label>
                      <div class="row items-center no-wrap">
                        <div class="column">
                          <q-avatar color="primary" size="40px">
                            <img v-if="store.user.img" :src="store.user.img" />
                            <template v-else>
                              {{ store.user.username.charAt(0).toUpperCase() }}
                            </template>
                          </q-avatar>
                        </div>
                        <div class="q-mx-sm" />
                        <div class="column">
                          <q-item-label class="text-dark text-left text-weight-regular">
                            {{ store.user.username }}
                          </q-item-label>
                          <q-item-label caption class="text-dark1">{{
                            store.user.email
                          }}</q-item-label>
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
                    <div class="row">
                      <div class="col-12">
                        <q-list>
                          <q-item
                            clickable
                            to="/user-authentication-and-management"
                            class="bg-info q-mb-sm dropdown-link"
                          >
                            <q-item-section>
                              <q-item-label class="">{{
                                $t(`MainLayout.links.UserAuthenticationAndManagement`)
                              }}</q-item-label>
                            </q-item-section>
                          </q-item>
                          <q-item clickable to="/" class="bg-info q-mb-sm dropdown-link">
                            <q-item-section>
                              <q-item-label class="">{{
                                $t(`MainLayout.links.Index`)
                              }}</q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
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
            <div class="flex justify-between items-center lt-md q-ml-auto">
              <div
                v-if="Object.keys(store.user).length !== 0"
                class="flex flex-center lt-md"
              >
                <q-btn-dropdown no-caps dropdown-icon="expand_more" class="avatar-btn">
                  <template v-slot:label>
                    <div class="row items-center no-wrap">
                      <q-avatar color="primary" size="30px">
                        <img v-if="store.user.img" :src="store.user.img" />
                        <template v-else>
                          {{ store.user.username.charAt(0).toUpperCase() }}
                        </template>
                      </q-avatar>
                    </div>
                  </template>

                  <div class="row no-wrap q-pa-md">
                    <div class="column">
                      <q-item-section>
                        <q-item-label class="text-weight-regular">
                          {{ store.user.username }}
                        </q-item-label>
                        <q-item-label caption class="">{{
                          store.user.email
                        }}</q-item-label>
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

                  <div class="row">
                    <div class="col-12">
                      <q-list>
                        <q-item
                          clickable
                          to="/user-authentication-and-management"
                          class="bg-info q-mb-sm dropdown-link"
                        >
                          <q-item-section>
                            <q-item-label class="">{{
                              $t(`MainLayout.links.UserAuthenticationAndManagement`)
                            }}</q-item-label>
                          </q-item-section>
                        </q-item>
                        <q-item clickable to="/" class="bg-info q-mb-sm dropdown-link">
                          <q-item-section>
                            <q-item-label class="">{{
                              $t(`MainLayout.links.Index`)
                            }}</q-item-label>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                  </div>
                </q-btn-dropdown>
              </div>
              <q-btn
                flat
                dense
                round
                icon="menu"
                aria-label="Menu"
                @click="toggleLeftDrawer"
                class="lt-md"
                color="dark"
              />
            </div>
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="leftDrawerOpen"
        class="left-sidebar q-py-xl flex column justify-betweeen no-wrap"
        show-if-above
        :width="350"
      >
        <!-- Desktop -->
        <q-list class="q-mx-lg gt-sm">
          <!-- <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" /> -->
          <!-- <q-item class="q-mb-md" clickable to="/user-authentication-and-management">
            <q-item-section avatar>
              <q-icon size="30px" name="img:/static/user-management.svg" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-white">{{
                $t(`MainLayout.links.UserAuthenticationAndManagement`)
              }}</q-item-label>
            </q-item-section>
          </q-item> -->
          <q-item class="q-mb-md" clickable to="/file-management">
            <q-item-section avatar>
              <q-icon size="30px" name="img:/static/file-management.svg" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-white">{{
                $t(`MainLayout.links.FileManagement`)
              }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item class="q-mb-md" clickable to="/index-preparation">
            <q-item-section avatar>
              <q-icon size="30px" name="img:/static/index-preparation.svg" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-white">{{
                $t(`MainLayout.links.Services`)
              }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-list class="q-mx-lg lt-md">
          <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" />
        </q-list>
        <img
          class="q-my-auto gt-sm q-mx-lg"
          style="height: 200px; object-fit: contain; align-self: start"
          src="/static/sidebar.png"
          alt=""
        />
        <q-btn
          class="q-mx-md text-capitalize q-mt-auto"
          rounded
          padding="16px 20px"
          color="white"
          outline
          icon="img:/static/logout.png"
          label="Logout"
          @click="logout"
        />
      </q-drawer>

      <q-page-container>
        <div class="cover">
          <div class="flex items-center full-width lt-md q-mb-md">
            <q-select
              v-model="projectName"
              :placeholder="$t('pages.FileManagementPage.projectName')"
              class="language-dropdown q-mr-md"
              :options="userProjects"
              option-value="name"
              option-label="name"
              emit-value
              outlined
              color="white"
              icon-color="white"
              text-color="dark"
              dense
            />
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
          <div class="row q-mb-md q-col-gutter-md items-center">
            <!-- <div class="col-12 col-sm-4 col-md-3">
              <q-select
                v-model="projectName"
                :placeholder="$t('pages.FileManagementPage.projectName')"
                class="q-mb-md"
                bg-color="white"
                borderless
                :options="userProjects"
                option-value="name"
                option-label="name"
                emit-value
              />
            </div> -->
            <div class="col-12">
              <q-stepper
                v-model="step"
                alternative-labels
                ref="stepper"
                color="primary"
                animated
                flat
              >
                <!-- <q-step
                :name="1"
                title="Create Project"
                icon="fiber_manual_record"
                :done="step > 1"
                @click="$router.push('/')"
              />
              <q-step
                :name="2"
                title="Upload Files"
                icon="fiber_manual_record"
                :done="step > 2"
                @click="$router.push('/file-management')"
              />
              <q-step
                :name="3"
                title="ProjectView & Training"
                icon="fiber_manual_record"
                :done="step > 3"
                @click="$router.push('/')"
              />
              <q-step
                :name="4"
                title="Service"
                icon="fiber_manual_record"
                :done="step > 4"
                @click="$router.push('/index-preparation')"
              /> -->
                <q-step
                  :name="1"
                  title="Create Project"
                  icon="fiber_manual_record"
                  :done="step > 1"
                  @click="stepClicked"
                />
                <q-step
                  :name="2"
                  title="Upload Files"
                  icon="fiber_manual_record"
                  :done="step > 2"
                  @click="stepClicked"
                />
                <!-- <q-step
                  :name="3"
                  title="ProjectView & Training"
                  icon="fiber_manual_record"
                  :done="step > 3"
                  @click="stepClicked"
                /> -->
                <q-step
                  :name="3"
                  title="Service"
                  icon="fiber_manual_record"
                  :done="step > 3"
                  @click="stepClicked"
                />
              </q-stepper>
            </div>
          </div>
          <router-view />
        </div>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { defineComponent, ref, watch, computed, onMounted } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';
import { useRouter, useRoute } from 'vue-router';
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
    const step = ref(1);
    const leftDrawerOpen = ref(false);
    const search = ref('');
    const router = useRouter();
    const route = useRoute();

    const store = useAuthStore();
    const serviceStore = useServiceStore();
    const projectStore = useProjectStore();
    const loading = ref(false);
    const error = ref(null);
    const userProjects = computed(() => projectStore.userProjects);
    const projectName = ref(
      projectStore.selectedProject ? projectStore.selectedProject : ''
    );

    const { locale } = useI18n({ useScope: 'global' });

    function logout() {
      localStorage.removeItem('jarvixUser');
      localStorage.setItem('currentSelectedProject', projectStore.selectedProject);
      store.user = {};
      serviceStore.chatHistory = [];
      router.push('/auth/login');
    }
    watch(locale, (val) => {
      if (val == 'EN') {
        serviceStore.currentLanguage = 'EN';
      } else if (val == 'zhHans') {
        serviceStore.currentLanguage = 'ZH_CN';
      } else {
        serviceStore.currentLanguage = 'ZH_TW';
      }
    });
    const localeOptions = ref([
      { value: 'EN', label: 'english' },
      { value: 'zhHans', label: 'chineeseSimplified' },
      { value: 'zhHant', label: 'chineeseTraditional' },
    ]);
    const selectedLabel = (item) => {
      const option = localeOptions.value.find((i) => i.value == item);
      return option.label;
    };
    watch(projectName, async (projectValue) => {
      if (projectValue) {
        projectStore.selectedProject = projectValue;
        projectStore.projectFiles = [];
        await listProjectFiles();
        await getSessions();
      }
    });
    async function getSessions() {
      try {
        error.value = null;
        loading.value = true;
        if (projectStore.selectedProject) {
          const res = await serviceStore.getSessions();
        } else {
          return;
        }
      } catch (err) {
        console.log(err);
        error.value = err.response.status + ' - ' + err.response.statusText;
      } finally {
        loading.value = false;
      }
    }
    async function listProjectFiles() {
      try {
        error.value = null;
        loading.value = true;
        const res = await projectStore.listProjectFiles({
          project_name: projectName.value,
        });
      } catch (err) {
        console.log(err);
        error.value = err.response.status + ' - ' + err.response.statusText;
      } finally {
        loading.value = false;
      }
    }
    watch(route, (newVal) => {
      if (newVal.path == '/') {
        step.value = 1;
      } else if (newVal.path == '/file-management') {
        step.value = 2;
      } else if (newVal.params.id && newVal.name == 'SingleProject') {
        step.value = 3;
        console.log('Here');
      } else if (newVal.path == '/index-preparation') {
        step.value = 4;
      }
    });
    onMounted(() => {
      if (route.path == '/') {
        step.value = 1;
      } else if (route.path == '/file-management') {
        step.value = 2;
      } else if (route.params.id && route.name == 'SingleProject') {
        step.value = 3;
      } else if (route.path == '/index-preparation') {
        step.value = 4;
      }
    });
    function stepClicked() {
      console.log('Clicked');
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
      localeOptions,
      selectedLabel,
      projectName,
      getSessions,
      listProjectFiles,
      userProjects,
      step,
      stepClicked,
    };
  },
});
</script>

<style lang="scss">
.q-drawer--left {
  // border-radius: 0px 20px 20px 0px;
  background: $primary;
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
  // border: 0.5px solid #fff;
  // .q-field__native {
  //   color: #fff !important;
  //   span {
  //     color: #fff !important;
  //   }
  // }
  // .q-select__dropdown-icon {
  //   color: #fff;
  // }
}

.q-header .q-field__control {
  height: 30px;
}
.q-router-link--active {
  background: #fff;
  border-radius: 44px;
  border-bottom: 3px solid $primary;
  .q-item__label {
    color: #005055 !important;
  }
  img {
    filter: invert(23%) sepia(1%) saturate(7101%) hue-rotate(147deg) brightness(25%)
      contrast(102%);
  }
}
.q-router-link--active.dropdown-link{
  border-radius: 0px;
  // border-bottom: 0px;
}
.q-stepper__step-inner {
  padding: 0px !important;
}
.q-stepper__header--alternative-labels .q-stepper__tab {
  padding-block: 16px;
  padding-inline: 16px;
  min-height: auto;
}
@media (max-width: 960px) {
  .q-stepper__header {
    flex-wrap: nowrap;
  }
  .q-stepper__header--alternative-labels .q-stepper__tab {
    padding: 10px;
    min-height: auto;
  }
  .q-stepper__title {
    font-size: 10px;
  }
}
@media (max-width: 380px) {
  .q-stepper__title {
    font-size: 8px;
  }
}
.avatar-btn {
  .q-btn-dropdown__arrow {
    display: none !important;
  }
}
</style>
