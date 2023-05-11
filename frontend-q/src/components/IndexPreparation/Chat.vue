<template>
  <div class="q-py-lg">
    <div class="chat-wrapper">
      <q-scroll-area class="chat-area">
        <q-chat-message
          v-for="n in 3"
          :key="n"
          bg-color="white"
          text-color="dark-page"
          size="6"
          :text="[
            `Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euu
            ismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim
            veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea `,
          ]"
          class="q-mb-md"
        />
        <q-chat-message
          v-for="n in 3"
          :key="n"
          text-color="dark-page"
          bg-color="info"
          sent
          class="q-mb-md"
          size="6"
          :text="[
            `Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euu
            ismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim
            veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea `,
          ]"
        />
      </q-scroll-area>
      <q-input
        rounded
        bg-color="white"
        standout="bg-white text-dark"
        class="elevation-0 q-mr-md full-width"
        v-model="search"
        placeholder="Search"
        :input-style="{ color: '#878787' }"
      >
        <template v-slot:append>
          <q-icon name="img:src/assets/send.svg" />
        </template>
      </q-input>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>

<style lang="scss" >
.q-field--standout .q-field__control {
  box-shadow: none !important;
  &::before,
  &::after {
    display: none;
  }
}
.chat-area {
  height: calc(100vh - 300px);
}
</style>
