<template>
  <div class="row">
    <div class="col-12">
      <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-bold text-dark">All Files</div>
          <q-separator class="q-my-lg" />
          <div class="row q-col-gutter-md">
            <div v-for="n in 8" :key="n" class="col-12 col-sm-4 col-md-3">
              <div class="img-container">
                <!-- <img src="~/assets/file-img.png" class="full-width" alt="" /> -->
                <q-btn
                  color="transparent"
                  class="menu-icon"
                  icon="more_vert"
                  unelevated
                  round
                  size="md"
                >
                  <q-menu>
                    <q-list style="min-width: 100px">
                      <q-item clickable v-close-popup>
                        <q-item-section>Edit</q-item-section>
                      </q-item>
                      <q-item clickable v-close-popup>
                        <q-item-section>Delete</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </div>
              <div class="text-dark text-h6 text-weight-bold">
                Name of the fle
              </div>
              <div class="text-dark-page text-body">File type: mp4</div>
            </div>
          </div>
          <q-btn
            color="primary"
            unelevated
            class="text-dark text-capitalize q-mt-lg"
            text-color="dark"
            style="width: 150px"
            >Index All Files</q-btn
          >
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
