<template>
  <div class="q-py-lg">
    <div class="chat-wrapper">
      <q-scroll-area class="chat-area">
        <q-chat-message
          v-for="(message, i) in chatHistory"
          :key="i"
          :bg-color="message.type === 'user-message' ? 'info' : 'white'"
          text-color="dark-page"
          size="6"
          :text="[message.text]"
          :sent="message.type === 'user-message' ? true : false"
          class="q-mb-md"
        />
      </q-scroll-area>
      <q-form @submit.prevent="submitQuery">
        <q-input
          rounded
          bg-color="white"
          standout="bg-white text-dark"
          class="elevation-0 q-mr-md full-width"
          v-model="queryText"
          placeholder="Search"
          :input-style="{ color: '#878787' }"
        >
          <template v-slot:append>
            <q-icon name="/send.svg" />
          </template>
        </q-input>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useServiceStore } from "src/stores/service";
import { useRoute } from "vue-router";
const store = useServiceStore();
const chatHistory = computed(() => store.chatHistory);
const loading = ref(false);
const error = ref(null);
const queryText = ref("");
const submitQuery = async () => {
  try {
    error.value = null;
    loading.value = true;
    store.addUserMessage(queryText.value);
    const res = await store.submitQuery({
      query: queryText.value,
    });
    console.log(res);
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
  } finally {
    loading.value = false;
    queryText.value = "";
  }
};
</script>

<style lang="scss">
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
