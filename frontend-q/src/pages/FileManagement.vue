<template>
  <div>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-9">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section class="q-pa-lg">
            <div class="text-h6 text-weight-bold text-dark">Uploaded Files</div>
            <q-separator class="q-my-lg" />
            <div class="row q-col-gutter-md">
              <div v-for="n in 6" :key="n" class="col-12 col-sm-6 col-md-4">
                <div class="img-container">
                  <img src="~/assets/file-img.png" class="full-width" alt="" />
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
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 10px">
          <q-card-section class="q-pa-md">
            <div class="text-h6 text-weight-bold text-dark">
              Upload New File
            </div>
            <q-separator class="q-my-lg" />
            <q-btn
              outline
              color="grey-3"
              class="full-width"
              style="height: 200px"
              rounded
            >
              <q-icon name="add" color="dark"></q-icon>
            </q-btn>
            <q-btn
              color="primary"
              unelevated
              class="text-dark text-capitalize q-mt-lg"
              text-color="dark"
              style="width: 120px"
              >Upload</q-btn
            >
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

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
