<template>
  <div class="q-py-lg">
    <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
      <q-card-section class="q-pa-lg">
        <div class="text-h6 text-weight-bold text-dark">Question : 1</div>
        <q-separator class="q-my-lg" />
        <div class="text-body text-dark">
          Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
          nonummy nibh euismod tincidunt ut laoreet?
        </div>
      </q-card-section>
    </q-card>
    <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
      <q-card-section class="q-pa-lg">
        <div class="text-h6 text-weight-bold text-dark">
          All Possible Answers
        </div>
        <q-separator class="q-my-lg" />
        <div v-for="n in 4" :key="n" class="q-mb-md">
          <div class="text-body text-dark text-weight-medium">
            Option {{ n }} :
          </div>
          <div class="text-body text-dark q-ml-md text-weight-regular">
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
            nonummy nibh euismod tincidunt ut laoreet? dolore magna aliquam erat
            volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
            ullamcorper suss cipit lobortis nisl ut aliquip ex ea commodo
            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate
          </div>
        </div>
      </q-card-section>
    </q-card>
    <q-btn
      color="primary"
      unelevated
      class="text-dark text-capitalize q-mt-lg"
      text-color="dark"
      style="width: 200px"
      >Add New Questions</q-btn
    >
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

<style scoped></style>
