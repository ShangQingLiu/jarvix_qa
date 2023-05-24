<template>
  <div class="q-py-lg">
    <div class="chat-wrapper">
      <q-scroll-area ref="scrollAreaRef" class="chat-area">
        <div v-for="(chat, i) in chatHistory" :key="i">
          <q-chat-message
            v-for="(message, j) in Object.values(chat)"
            :key="j"
            :bg-color="j === 0 ? 'info' : 'white'"
            text-color="dark-page"
            size="6"
            :text="[message]"
            :sent="j === 0 ? true : false"
            class="q-mb-md"
          />
        </div>
        <!-- <div v-if="!loading" class="flex flex-center q-py-lg">
         <q-spinner-oval color="primary" size="3rem" />
        </div> -->
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
          :disable="projectName ? false : true"
        >
          <template v-slot:append>
            <q-icon v-if="!loading" name="/send.svg" />
            <q-spinner v-else color="negative" size="2em" />
          </template>
        </q-input>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, nextTick } from 'vue';
import { useServiceStore } from 'src/stores/service';
import { useQuasar } from 'quasar';
import { useProjectStore } from 'src/stores/project';

const $q = useQuasar();
const store = useServiceStore();
const projectStore = useProjectStore();
const projectName = computed(() => projectStore.selectedProject);
const chatHistory = computed(() => store.chatHistory);
const loading = ref(false);
const error = ref(null);
const queryText = ref('');
const scrollAreaRef = ref(null);
const submitQuery = async () => {
  try {
    error.value = null;
    loading.value = true;
    store.addUserMessage(queryText.value);
    await nextTick();
    // Scrolling at the bottom of Question List
    const scrollArea = scrollAreaRef.value;
    const scrollTarget = scrollArea.getScrollTarget();
    const duration = 300;
    scrollAreaRef.value.setScrollPosition(
      'vertical',
      scrollTarget.scrollHeight,
      duration
    );
    const res = await store.submitQuery({
      query: queryText.value,
      sessionFrom: 'ChatRoom',
    });
    await nextTick();
    scrollAreaRef.value.setScrollPosition(
      'vertical',
      scrollTarget.scrollHeight,
      duration
    );
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
    $q.notify({
      message: error.value ? error.value : 'Something Went Wrong',
      position: 'top-right',
      color: 'negative',
    });
  } finally {
    loading.value = false;
    queryText.value = '';
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
  height: calc(100vh - 350px);
}
</style>
