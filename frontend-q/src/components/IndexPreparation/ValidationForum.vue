<template>
  <div class="row q-col-gutter-md">
    <div class="col-12">
      <q-card flat class="bg-white q-mb-lg">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">
            Add your Question (Must end with . )
            <!-- {{ $t('pages.IndexPreparation.Question.questions.title') }} -->
          </div>
          <q-separator class="q-my-lg" />
          <q-input
            v-model="queryText"
            :placeholder="$t('pages.IndexPreparation.Question.questions.queryText')"
            class="q-mb-md"
            bg-color="accent"
            :input-style="{ padding: '20px 23px' }"
            borderless
            dense
            type="textarea"
            hint="Must add . after each question / End of question"
          />

          <div class="flex">
            <q-btn
              color="primary"
              unelevated
              class="text-dark text-capitalize"
              text-color="white"
              @click="previewQuestionsList"
            >
              <!-- {{ $t('pages.IndexPreparation.Question.questions.questionBtn') }} -->

              Preview Question Document
            </q-btn>
            <!-- <q-spinner v-if="loading" class="q-ml-auto" color="negative" size="2em" /> -->
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div v-if="questionsList.length > 0" class="col-12">
      <q-card flat class="bg-white q-mb-lg">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">
            Validation Form
            <!-- {{ $t('pages.IndexPreparation.Question.questions.title') }} -->
          </div>
          <q-separator class="q-my-lg" />
          <div v-if="loading" class="q-py-lg flex justify-center">
            <q-spinner color="dark" size="3em" />
          </div>
          <q-scroll-area class="bg-accent q-pa-lg" style="height: 600px">
            <div v-for="(question, i) in questionsList" :key="i" class="q-mb-md">
              <div class="flex items-center">
                <div class="text-body text-dark text-weight-bold">Q {{ i + 1 }} :</div>
                <div class="text-body text-dark q-ml-md text-weight-regular">
                  {{ question }}
                </div>
              </div>
            </div>
          </q-scroll-area>
          <div class="flex q-mt-md">
            <q-btn
              color="primary"
              unelevated
              class="text-dark text-capitalize"
              text-color="white"
              @click="submitQuestionsList"
            >
              Submit
            </q-btn>
            <q-btn
              color="primary"
              unelevated
              class="text-dark text-capitalize q-ml-xl"
              text-color="white"
              type="submit"
            >
              Upload Questions Document
            </q-btn>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12" v-if="rows.length > 0">
      <q-card flat class="bg-white q-mb-lg">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">Validation Form</div>
          <q-separator class="q-my-lg" />
          <q-scroll-area class="bg-white q-pa-lg" style="height: 600px">
            <q-table :rows="rows" hide-bottom :columns="columns" row-key="name">
              <template v-slot:header-cell="props">
                <q-th class="" :props="props">
                  {{ props.col.label }}
                </q-th>
              </template>
              <template v-slot:body="props">
                <q-tr :props="props">
                  <q-td key="question" :props="props">
                    {{ props.row.question }}
                  </q-td>
                  <q-td key="expect_answer" :props="props">
                    {{ props.row.expect_answer }}
                  </q-td>
                  <q-td key="query_answer" :props="props">
                    {{ props.row.query_answer.split(',')[0] }}
                  </q-td>
                  <q-td key="is_correct" :props="props">
                    {{ props.row.is_correct }}
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </q-scroll-area>
        </q-card-section>
        <div class="q-pa-lg">
          <q-card-section class="q-pa-lg">
            <div class="text-subtitle1 text-dark">
              Summary Score:
              <span class="text-weight-bold"
                >{{ store.validationForumContent.correct_number }}/{{
                  store.validationForumContent.total_number
                }}</span
              >
            </div>
          </q-card-section>
        </div>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue';
import { useServiceStore } from 'src/stores/service';
import { useRoute } from 'vue-router';
const columns = [
  {
    name: 'question',
    label: 'Question',
    align: 'left',
    field: 'question',
  },
  {
    name: 'expect_answer',
    align: 'center',
    label: 'Expected Answer',
    field: 'expect_answer',
  },
  { name: 'query_answer', label: 'Query Answer', field: 'query_answer', align: 'center' },
  {
    name: 'is_correct',
    label: 'Correct(True/False)',
    field: 'is_correct',
    align: 'center',
  },
];
// const rows = [
//   {
//     question: 'Is there any fines in the NDA document',
//     expect_answer: ' No',
//     query_answer: 'No, there is no mention of fines in the NDA document.',
//     is_correct: true,
//   },
//   {
//     question: 'Is the agreement a one-direction agreement',
//     expect_answer: ' Yes',
//     query_answer: 'Yes, the agreement is a one-direction agreement.',
//     is_correct: false,
//   },
//   {
//     question: 'Is there any fines in the NDA document',
//     expect_answer: ' No',
//     query_answer: 'No, there is no mention of fines in the NDA document.',
//     is_correct: true,
//   },
//   {
//     question: 'Is the agreement a one-direction agreement',
//     expect_answer: ' Yes',
//     query_answer: 'Yes, the agreement is a one-direction agreement.',
//     is_correct: false,
//   },
// ];
const store = useServiceStore();
const loading = ref(false);
const error = ref(null);
const queryText = ref('');
const questionsList = ref([]);
const rows = ref([]);
const submitQuestionsList = async () => {
  try {
    error.value = null;
    loading.value = true;
    const res = await store.submitValidationForum({
      query: queryText.value,
      sessionFrom: 'ValidationForum',
    });
    rows.value = res.answer;
  } catch (err) {
    console.log(err);
    error.value = err.response.status + ' - ' + err.response.statusText;
  } finally {
    loading.value = false;
    questionsList.value = [];
  }
};
// Getting Questions List
const previewQuestionsList = async () => {
  console.log(queryText.value);
  questionsList.value = queryText.value.split('.');
  questionsList.value.pop();
  store.validationQuestions = questionsList.value;
};
</script>

<style scoped></style>
