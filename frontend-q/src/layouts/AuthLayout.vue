<template>
  <div class="">
    <q-layout view="hHh lpR fFf">
      <div class="row auth-wrapper relative-position items-center">
        <div class="col-12 gt-sm full-height col-md-5 bg-primary">
          <div
            class="flex column auth-wrapper relative-position full-height justify-center items-center align-center"
          >
            <div
              class="logo-container q-my-xl"
              style="align-self: flex-end; padding-right: 60px"
            >
              <img style="max-width: 200px" src="/static/logo-white.png" />
            </div>
            <p class="text-white welcome-text">
              {{ $t(`AuthLayout.welcomeText`) }}
            </p>
            <!-- Info -->
            <!-- <q-btn color="white" class="info-btn" flat icon="help">
              <q-menu>
                <div style="max-width: 300px" class="row no-wrap q-pa-md">
                  <div class="column">
                    <p>
                      BauMa is the system aims to become your private assistant to answer
                      the question regards all your data, you can follow the pipeline 1.
                      Create a project 2. Upload files you want to ask for 3. Click for
                      training and wait until it finish 4. Enjoy the service Chatbot!
                    </p>
                  </div>
                </div>
              </q-menu>
            </q-btn> -->
          </div>
        </div>
        <div class="col-12 col-md-7 full-height">
          <div class="q-px-xl">
            <div class="flex justify-between items-center full-height full-width q-mb-md">
              <q-select
                v-model="locale"
                :options="localeOptions"
                outlined
                text-color="dark"
                emit-value
                map-options
                style="max-width: 160px"
                dense
                class="language-dropdown auth-layout-language-dropdown"
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
            <div class="full-height">
              <router-view />
            </div>
          </div>
        </div>
      </div>
    </q-layout>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useServiceStore } from 'src/stores/service';

import { useI18n } from 'vue-i18n';

export default defineComponent({
  name: 'AuthLayout',

  components: {},

  setup() {
    const router = useRouter();
    const store = useAuthStore();
    const serviceStore = useServiceStore();
    const { locale } = useI18n({ useScope: 'global' });
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

    return {
      store,
      locale,
      localeOptions,
      selectedLabel,
    };
  },
});
</script>

<style lang="scss">
.bg-linear {
  background: linear-gradient(90deg, #005055 0%, #006464 99.99%);
  background: linear-gradient(90deg, #005055 0%, #006464 99.99%);
}
.auth-wrapper {
  min-height: 100vh;
}
.info-btn {
  position: absolute;
  bottom: 20px;
  left: 20px;
}
.auth-layout-language-dropdown {
  position: absolute;
  top: 20px;
  right: 20px;
}
</style>
<style lang="scss" scoped>
.welcome-text {
  font-size: 26px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  max-width: 480px;
  text-align: right;
}
</style>
