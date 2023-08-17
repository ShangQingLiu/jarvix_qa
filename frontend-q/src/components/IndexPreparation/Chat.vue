<template>
  <div>
    <q-scroll-area ref="scrollAreaRef" class="chat-area overflow-y-auto">
      <!-- <div>
        {{
          formatMessage(
            `Lorem ipsum dolor sit, amet consectetur adipisicing elit. Voluptatem culpa laborum quisquam illum quod corrupti! `,
            true
          )
        }}
      </div> -->
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
        >
          <template #stamp>
            <div v-if="j === 1" class="flex justify-end q-my-none">
              <q-icon name="info" size="20px" color="dark1">
                <q-menu>
                  <div
                    style="max-width: 250px"
                    class="row no-wrap q-pa-md bg-accent text-dark"
                  >
                    <div class="column">
                      <div class="text-dark text-weight-bold">
                        {{ $t('Extra.reference') }}
                      </div>
                      <div
                        class="q-mb-sm text-dark1"
                        style="
                          white-space: nowrap;
                          text-overflow: ellipsis;
                          display: block;
                          width: 230px;
                          overflow: hidden;
                        "
                      >
                        2023 annual car saling dataset
                      </div>
                      <div class="flex justify-between items-center">
                        <div  class="text-dark-page">{{ $t('Extra.download') }}</div>
                        <q-btn
                          class="text-capitalize"
                          flat
                          style="color: #45b3b2"
                          :label="$t('Extra.abstractBtn')"
                          @click="abstractModal = !abstractModal"
                        />
                      </div>
                    </div>
                  </div>
                </q-menu>
              </q-icon>
            </div>
          </template>
        </q-chat-message>
      </div>
      <!-- <div
          v-for="(message, j) in Object.values(chat)"
          :key="j"
          :bg-color="j === 0 ? 'user-chat' : 'response'"
          text-color="dark-page"

          :sent="j === 0 ? true : false"
          class="q-mb-md chat-message-content col-9 dark-page"
          :class="{ 'last-message': chatHistory.length - 1 === i && j === 1, 'bg-user-chat': j === 0, 'bg-response': j === 1, 'items-end': j === 0, }"

        >
        {{ formatMessage(message, chatHistory.length - 1 === i && j === 1 ? true : false) }}
        </div> -->

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
        :placeholder="$t('Extra.chatPlaceholder')"
        :input-style="{ color: '#878787' }"
        outlined
        color="dark1"
        :disable="loading"
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

    <q-dialog v-model="abstractModal">
      <q-card>
        <q-card-section>
          <div class="text-h6 text-center text-weight-bold">Abstract Reference</div>
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 50vh" class="scroll">
          <p v-for="n in 15" :key="n">Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.</p>
        </q-card-section>

        <q-separator />

        <q-card-actions align="center">
          <q-btn no-caps outline label="Download Full Document" color="primary" v-close-popup />
          <q-btn no-caps label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
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
const abstractModal = ref(false);

const scrollToBottom = async () => {
  await nextTick();
  // Scrolling at the bottom of Question List
  const scrollArea = scrollAreaRef.value;
  const scrollTarget = scrollArea.getScrollTarget();
  const duration = 0;
  scrollAreaRef.value.setScrollPosition('vertical', scrollTarget.scrollHeight, duration);
};
const submitQuery = async () => {
  if (projectName.value) {
    try {
      error.value = null;
      loading.value = true;
      await store.submitQuery(
        {
          query: queryText.value,
          sessionFrom: 'ChatRoom',
        },
        scrollToBottom
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
  height: calc(100vh - 350px);
}
.append-content .border-left {
  border-left: 1px solid $dark-page;
}
</style>
