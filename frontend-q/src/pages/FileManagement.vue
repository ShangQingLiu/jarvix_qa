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
            <div v-if="loading" class="q-py-lg flex justify-center">
              <q-spinner color="dark" size="3em" />
            </div>
            <div v-if="error" class="q-py-sm flex justify-center">
              <div class="text-h6 text-negative">
                {{ error }}
              </div>
            </div>
            <div v-if="success" class="q-py-sm flex justify-center">
              <div class="text-h6 text-primary">
                {{ success }}
              </div>
            </div>
            <q-btn
              unelevated
              color="bg-accent"
              class="full-width bg-accent"
              style="height: 200px"
              @click="loadLocalFiles"
              v-if="!loading"
            >
              <q-icon name="add" color="dark"></q-icon>
            </q-btn>
            <input
              accept=".docx,.pdf,.html,.mp3,.m4a"
              @change="uploadFiles"
              multiple
              type="file"
              ref="filesRef"
              style="display: none"
            />
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize q-mt-lg"
              text-color="white"
              style="width: 120px"
              v-if="!loading"
              >Upload</q-btn
            >
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from "src/boot/axios";
export default {
  data() {
    return {
      filesRef: null,
      uploadingFiles: false,
      uploadedFiles: [],
      loading: false,
      error: null,
      success: null,
    };
  },
  methods: {
    loadLocalFiles() {
      this.$refs.filesRef.click();
    },
    async uploadFiles(e) {
      try {
        this.loading = true;
        this.uploadedFiles = [];
        const formData = new FormData();
        let res;
        for (var i = 0; i < this.$refs.filesRef.files.length; i++) {
          let file = this.$refs.filesRef.files[i];
          formData.append("files", file);
          res = await api.post(`file/upload?project_name=project`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        }
        // let files = this.$refs.filesRef.files;
        // console.log(files);
        // formData.append("files", files);
        // console.log("Here");
        // const { data } = await api.post(
        //   `file/upload?project_name=project`,
        //   formData,
        //   {
        //     headers: {
        //       "Content-Type": "multipart/form-data",
        //     },
        //   }
        // );
        console.log(res);
        // this.success = data.message;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },
    // async removeImage(img) {
    //   try {
    //     const res = await axios.delete(`/medicalreportsimages/${img.id}/`);
    //   } catch (error) {
    //     console.log(error);
    //   }
    //   this.uploadedFiles = this.uploadedFiles.filter(
    //     (image) => image.id !== img.id
    //   );
    // },
  },
};
</script>
<style lang="scss" scoped></style>
