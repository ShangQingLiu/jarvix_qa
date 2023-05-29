<template>
  <div class="">
    <q-layout view="hHh lpR fFf">
      <div class="row auth-wrapper items-center">
        <div class="col-12 gt-sm full-height col-md-5 bg-linear">
          <div
            class="flex column auth-wrapper full-height justify-center items-center align-center"
          >
            <div class="logo-container q-my-xl text-center">
              <img style="max-width: 200px" src="/static/logo.svg" />
            </div>
            <p class="text-white">
              {{ $t(`AuthLayout.welcomeText`) }}
            </p>
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
                class="language-dropdown"
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
      val == 'en-US'
        ? (serviceStore.currentLanguage = 'EN')
        : (serviceStore.currentLanguage = 'ZH');
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
</style>
