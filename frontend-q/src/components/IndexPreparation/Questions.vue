<template>
  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-6">
      <q-card flat class="bg-white q-mb-lg">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">Add New Question</div>
          <q-separator class="q-my-lg" />
          <q-form @submit.prevent="submitQuery">
            <q-input
              v-model="queryText"
              placeholder="Type your question here..."
              class="q-mb-md"
              bg-color="accent"
              :input-style="{ padding: '0px 23px' }"
              borderless
              dense
            />
            <q-select
              v-model="questionType"
              placeholder="Email"
              class="q-mb-md"
              bg-color="accent"
              :input-style="{ padding: '0px 23px' }"
              borderless
              dense
              :options="questionTypes"
            />

            <div class="flex">
              <q-btn
                color="primary"
                unelevated
                class="text-dark text-capitalize"
                text-color="white"
                style="width: 204px"
                type="submit"
                >Add Question</q-btn
              >
              <q-spinner
                v-if="loading"
                class="q-ml-auto"
                color="negative"
                size="2em"
              />
            </div>
          </q-form>
          <q-separator class="q-my-lg" />
          <q-scroll-area ref="scrollAreaRef" style="height: 300px">
            <div v-for="(message, i) in chatHistory" :key="i" class="q-mb-md">
              <div>
                <div class="text-body text-dark text-weight-bold">
                  Question {{ i + 1 }} :
                </div>
                <div class="text-body text-dark q-ml-md text-weight-regular">
                  {{ message.query }}
                </div>
              </div>
            </div>
          </q-scroll-area>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-md-6">
      <q-card flat class="bg-white q-mb-lg">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">
            All Possible Answers
          </div>
          <q-separator class="q-my-lg" />
          <q-scroll-area ref="scrollAreaRef2" style="height: 300px">
            <div v-for="(message, i) in chatHistory" :key="i" class="q-mb-md">
              <div>
                <div class="text-body text-dark text-weight-bold">
                  Answer {{ i + 1 }} :
                </div>
                <div class="text-body text-dark q-ml-md text-weight-regular">
                  {{ message.response }}
                </div>
              </div>
            </div>
          </q-scroll-area>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import { useServiceStore } from "src/stores/service";
import { useRoute } from "vue-router";
const store = useServiceStore();
const chatHistory = computed(() => store.chatHistory);
const loading = ref(false);
const error = ref(null);
const queryText = ref("");
const questionType = ref("");
const questionTypes = ref(["True/False"]);
const scrollAreaRef = ref(null);
const scrollAreaRef2 = ref(null);

const position = ref(1);
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
      "vertical",
      scrollTarget.scrollHeight,
      duration
    );
    const res = await store.submitQuery({
      query: queryText.value,
    });
    await nextTick();

    // Scrolling at the bottom of Answers List
    const scrollArea2 = scrollAreaRef2.value;
    const scrollTarget2 = scrollArea2.getScrollTarget();
    const duration2 = 300;
    scrollAreaRef2.value.setScrollPosition(
      "vertical",
      scrollTarget2.scrollHeight,
      duration2
    );
  } catch (err) {
    console.log(err);
    error.value = err.response.status + " - " + err.response.statusText;
  } finally {
    loading.value = false;
    queryText.value = "";
  }
};
</script>

<style scoped></style>
