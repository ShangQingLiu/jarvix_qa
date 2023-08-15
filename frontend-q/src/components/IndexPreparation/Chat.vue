<template>
  <div>
    <q-scroll-area ref="scrollAreaRef" class="chat-area overflow-y-auto">
      <div v-for="(chat, i) in chatHistory" :key="i">
        <q-chat-message
          v-for="(message, j) in Object.values(chat)"
          :key="j"
          :bg-color="j === 0 ? 'user-chat' : 'response'"
          text-color="dark-page"
          size="9"
          :text="[message]"
          :sent="j === 0 ? true : false"
          class="q-mb-md chat-message-content"
          :class="{ 'last-message': chatHistory.length - 1 === i && j === 1 }"
        />
        <!-- <q-chat-message
          :bg-color="'response'"
          text-color="dark-page"
          size="9"
          :text="[message]"
          :sent="false"
          class="q-mb-md chat-message-content"
          v-else
        /> -->
      </div>
      <!-- <div v-if="!loading" class="flex flex-center q-py-lg">
         <q-spinner-oval color="primary" size="3rem" />
        </div> -->
    </q-scroll-area>

    <q-form @submit.prevent="submitQuery">
      <q-input
        rounded
        bg-color="transparent"
        standout="bg-white text-dark"
        class="elevation-0 q-mr-md full-width"
        v-model="queryText"
        placeholder="Type your question here..."
        :input-style="{ color: '#878787' }"
        outlined
        color="dark1"
      >
        <template v-slot:append>
          <div class="flex items-center append-content">
            <q-spinner-oval v-if="loading" color="dark-page" class="q-pr-md" size="2em" />
            <!-- <q-icon  /> -->
            <img
              v-if="!loading"
              src="/static/send.svg"
              class="q-pl-md border-left"
              alt=""
            />
          </div>
        </template>
      </q-input>
    </q-form>
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
  if (projectName.value) {
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
  } else {
    $q.notify({
      message: 'Please select project to start the chat',
      position: 'top-right',
      color: 'primary',
    });
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
  height: calc(100vh - 450px);
}
.append-content .border-left {
  border-left: 1px solid $dark-page;
}
</style>
