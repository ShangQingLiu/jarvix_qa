<template>
  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-6">
      <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">Add New Question</div>
          <q-separator class="q-my-lg" />
          <q-form>
            <q-input
              v-model="projectName"
              placeholder="User name"
              class="q-mb-md"
              bg-color="accent"
              :input-style="{ padding: '0px 23px' }"
              borderless
              dense
            />
            <q-input
              v-model="email"
              placeholder="Email"
              class="q-mb-md"
              type="email"
              bg-color="accent"
              :input-style="{ padding: '0px 23px' }"
              borderless
              dense
            />

            <q-btn
              color="primary"
              unelevated
              class="text-dark text-capitalize"
              text-color="white"
              style="width: 204px"
              >Add Question</q-btn
            >
          </q-form>
          <q-separator class="q-my-lg" />
          <q-scroll-area style="height: 300px">
            <div v-for="n in 4" :key="n" class="q-mb-md">
              <div class="text-body text-dark text-weight-bold">
                Answer {{ n }} :
              </div>
              <div class="text-body text-dark q-ml-md text-weight-regular">
                Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed
                diam nonummy nibh euismod tincidunt ut laoreet? dolore magna
                aliquam erat volutpat. Ut wisi enim ad minim veniam, quis
                nostrud exerci tation ullamcorper suss cipit lobortis nisl ut
                aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor
                in hendrerit in vulputate
              </div>
            </div>
          </q-scroll-area>
        </q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-md-6">
      <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">
            All Possible Answers
          </div>
          <q-separator class="q-my-lg" />
          <div v-for="n in 4" :key="n" class="q-mb-md">
            <div class="text-body text-dark text-weight-bold">
              Answer {{ n }} :
            </div>
            <div class="text-body text-dark q-ml-md text-weight-regular">
              Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
              nonummy nibh euismod tincidunt ut laoreet? dolore magna aliquam
              erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci
              tation ullamcorper suss cipit lobortis nisl ut aliquip ex ea
              commodo consequat. Duis autem vel eum iriure dolor in hendrerit in
              vulputate
            </div>
          </div>
        </q-card-section>
      </q-card>
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

<style scoped></style>
