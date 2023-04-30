<template>
  <div>
    <div class="row">
      <div class="col-12">
        <q-btn
          :color="panel === 'chat' ? 'primary' : 'white'"
          :text-color="panel === 'chat' ? 'dark' : 'dark-page'"
          unelevated
          style="height: 55px"
          icon="img:src/assets/chat.svg"
          label="Chat Room"
          @click="panel = 'chat'"
        />
        <q-btn
          :color="panel === 'questions' ? 'primary' : 'white'"
          :text-color="panel === 'questions' ? 'dark' : 'dark-page'"
          unelevated
          style="height: 55px"
          icon="img:src/assets/questions.svg"
          label="Question Form"
          @click="panel = 'questions'"
          class="q-ml-md"
        />
        <q-tab-panels v-model="panel" class="bg-transparent q-px-none q-py-lg">
          <q-tab-panel class="q-px-none" name="chat">
            <Chat />
          </q-tab-panel>

          <q-tab-panel class="q-px-none" name="questions">
            <Questions />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
    <all-files />
  </div>
</template>

<script>
import AllFiles from "../components/IndexPreparation/AllFiles.vue";
import Chat from "../components/IndexPreparation/Chat.vue";
import Questions from "../components/IndexPreparation/Questions.vue";
export default {
  components: { Questions, AllFiles, Chat },
  name: "IndexPreparation",
  data() {
    return {
      panel: "questions",
    };
  },
};
</script>
<style lang="scss" scoped>
.img-container {
  border-radius: 20px 20px 0px 0px;
  img {
    border-radius: 20px 20px 0px 0px;
  }
  position: relative;
  .menu-icon {
    position: absolute;
    top: 10px;
    right: 10px;
  }
}
</style>
