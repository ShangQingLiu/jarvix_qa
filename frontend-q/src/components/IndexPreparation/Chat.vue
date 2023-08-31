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
          :bg-color="'user-chat'"
          text-color="dark-page"
          size="9"
          :text="[chat.query]"
          :sent="false"
          class="q-mb-md chat-message-content"
        >
        </q-chat-message>

        <q-chat-message
          :bg-color="'response'"
          text-color="dark-page"
          size="9"
          :text="[chat.response]"
          :sent="true"
          class="q-mb-md chat-message-content"
        >
          <template #stamp>
            <div
              @click="getQuestionReference(chat.question_id)"
              class="flex justify-end q-my-none"
            >
              <q-icon name="info" size="20px" color="dark1">
                <q-menu>
                  <div
                    style="max-width: 250px"
                    class="row no-wrap q-pa-md bg-accent text-dark"
                  >
                    <div v-if="!isLoading" class="column">
                      <div class="text-dark text-weight-bold">
                        {{ $t('Extra.reference') }}
                      </div>
                      <div v-if="referenceContent.length">
                        <div
                          v-for="(content, i) in referenceContent"
                          class="flex no-wrap items-center"
                        >
                          <div
                            class="q-mb-sm text-dark1"
                            style="
                              white-space: nowrap;
                              text-overflow: ellipsis;
                              display: block;
                              width: 150px;
                              overflow: hidden;
                            "
                          >
                            {{ content.filename ? content.filename : content.score }}
                          </div>
                          <q-icon
                            class="q-ml-md cursor-pointer"
                            name="download"
                            size="20px"
                            color="dark1"
                            @click="
                              downloadProjectFile(
                                content.filename ? content.filename : content.score
                              )
                            "
                          />
                        </div>
                      </div>
                      <div
                        style="
                          white-space: nowrap;
                          text-overflow: ellipsis;
                          display: block;
                          width: 180px;
                          overflow: hidden;
                        "
                        v-else
                      >
                        {{ $t('Extra.noReference') }}
                      </div>
                      <div
                        v-if="referenceContent.length"
                        class="flex justify-end items-center"
                      >
                        <q-btn
                          class="text-capitalize"
                          flat
                          style="color: #45b3b2"
                          :label="$t('Extra.abstractBtn')"
                          @click="abstractModal = !abstractModal"
                        />
                      </div>
                    </div>
                    <div
                      v-else
                      class="flex justify-center items-center"
                      style="height: 150px; width: 200px"
                    >
                      <q-spinner-oval color="primary" size="2em" />
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
        <q-card-section class="q-pb-none">
          <div class="text-h6 text-center text-weight-bold">
          {{ $t('Extra.modalTitle') }}
          </div>
          <q-tabs
            v-model="existingAbstract"
            inline-label
            align="left"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            narrow-indicator
          >
            <q-tab
              v-for="(content, i) in referenceContent"
              :key="i"
              class="custom-tab"
              :name="
                getTabName(
                  content.filename ? content.filename : content.score,
                  content.score
                )
              "
              :label="content.filename ? content.filename : content.score"
            />
          </q-tabs>
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 50vh" class="scroll">
          <q-tab-panels
            v-model="existingAbstract"
            class="bg-transparent q-px-none q-py-none"
            animated
          >
            <q-tab-panel
              v-for="(content, i) in referenceContent"
              :key="i"
              class="q-px-none q-py-none"
              :name="
                getTabName(
                  content.filename ? content.filename : content.score,
                  content.score
                )
              "
            >
              <p>
                {{ content.text }}
              </p>
            </q-tab-panel></q-tab-panels
          >
        </q-card-section>

        <q-separator />

        <q-card-actions align="center">
          <q-btn
            no-caps
            outline
            :label="$t('Extra.downloadBtn')"
            color="primary"
            v-close-popup
            v-if="existingAbstract"
            @click="downloadProjectFile(existingAbstract)"
          />
          <q-btn no-caps :label="$t('Extra.closeBtn')" color="primary" v-close-popup />
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
import { api, apiFetch } from 'src/boot/axios';
import { guidGenerator } from 'src/utils';

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
const referenceContent = ref([]);
const isLoading = ref(false);
const existingAbstract = ref(null);
const emit = defineEmits(['disabled'])

const getTabName = (tabName, index) => {
  console.log(index);
  console.log(`${tabName.toString().split(' ').join('_')}${index}`);
  return `${tabName.toString().split(' ').join('_')}${index}`;
};
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
      emit('disabled', true);
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
      emit('disabled', false);

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
const getQuestionReference = async (id) => {
  try {
    isLoading.value = true;
    const { data } = await api.get(`/service/query/reference/${id}`);
    referenceContent.value = data;
    console.log(data);
    existingAbstract.value = getTabName(
      data[0].filename ? data[0].filename : data[0].score,
      data[0].score
    );
  } catch (error) {
    console.log(error);
  } finally {
    isLoading.value = false;
  }
};

const downloadProjectFile = async (file) => {
  try {
    error.value = null;
    loading.value = true;
    console.log('View Project File');
    const res = await projectStore.ViewProjectFile({
      project_name: projectStore.selectedProject,
      filename: file,
    });
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
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
