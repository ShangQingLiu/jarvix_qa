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
                <div class="wrapper bg-accent">
                  <div class="img-container">
                    <img
                      src="~/assets/file-img.png"
                      class="full-width"
                      alt=""
                    />
                  </div>
                  <div
                    class="flex full-width justify-between items-center q-px-md q-py-sm"
                  >
                    <div>
                      <div class="text-dark text-h6 text-weight-bold">
                        Name of the fle
                      </div>
                      <div class="text-dark-page text-body">File type: mp4</div>
                    </div>
                    <q-btn
                      round
                      color="negative"
                      unelevated
                      class="q-mx-xs"
                      icon="delete"
                      size="sm"
                    />
                  </div>
                </div>
              </div>
            </div>
            <q-btn
              unelevated
              color="primary"
              class="q-mt-md"
              text-color="white"
            >
              Re-Index
            </q-btn>
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
              unelevated
              color="bg-accent"
              class="full-width bg-accent"
              style="height: 200px"
              @click="uploadImage"
            >
              <q-icon name="add" color="dark"></q-icon>
            </q-btn>
            <input
              accept=".docx,.pdf,.html,.mp3,.m4a"
              @change="handleImage"
              multiple
              type="file"
              ref="imageFile"
              style="display: none"
            />
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize q-mt-lg"
              text-color="white"
              style="width: 120px"
              >Upload</q-btn
            >
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    uploadImage() {
      this.$refs.imageFile.click();
    },
    async handleImage(e) {
      try {
        this.uploadingImages = true;
        this.uploadedImages = [];
        const formData = new FormData();
        for (var i = 0; i < this.$refs.imageFile.files.length; i++) {
          let file = this.$refs.imageFile.files[i];
          formData.append("image", file);
          const res = await axios.post(`medicalreportsimages/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          this.uploadedImages.push(res.data);
        }
        console.log();
      } catch (err) {
        this.error = err;
      } finally {
        this.uploadingImages = false;
      }
    },
    async removeImage(img) {
      try {
        const res = await axios.delete(`/medicalreportsimages/${img.id}/`);
      } catch (error) {
        console.log(error);
      }
      this.uploadedImages = this.uploadedImages.filter(
        (image) => image.id !== img.id
      );
    },
  },
};
</script>
<style lang="scss" scoped></style>
