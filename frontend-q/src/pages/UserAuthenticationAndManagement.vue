<template>
  <div>
    <div class="row">
      <div class="col-12">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section>
            <q-form>
              <div class="row">
                <div class="col-6">
                  <q-input
                    dense
                    outlined
                    v-model="projectName"
                    placeholder="User name"
                    class="q-mb-md"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="password"
                    placeholder="Password"
                    class="q-mb-md"
                    type="password"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-xl">
                <q-btn
                  color="primary"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="dark"
                  >Login</q-btn
                >
                <q-btn
                  color="primary"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="dark"
                  >Sign Up</q-btn
                >
                <q-btn
                  color="negative"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="dark"
                  >Foget Password</q-btn
                >
              </div>
            </q-form>
          </q-card-section>
        </q-card>
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section>
            <q-form>
              <div class="row">
                <div class="col-6">
                  <q-input
                    dense
                    outlined
                    v-model="projectName"
                    placeholder="User name"
                    class="q-mb-md"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="email"
                    placeholder="Email"
                    class="q-mb-md"
                    type="email"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="password"
                    placeholder="Password"
                    class="q-mb-md"
                    type="password"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="confirmedPassword"
                    placeholder="Retype password"
                    class="q-mb-md"
                    type="password"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-md">
                <q-btn
                  color="primary"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="dark"
                  style="width: 204px"
                  >Sign Up</q-btn
                >
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-5">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">Project Name</div>
            <q-separator class="q-my-lg" />
            <q-list>
              <q-item
                v-for="n in 6"
                :key="n"
                class="q-py-none q-px-none list-item q-mb-lg"
              >
                <q-item-section top avatar>
                  <q-avatar size="45px">
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
                  </q-avatar>
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-dark">Randy Riley</q-item-label>
                  <q-item-label caption>randy.riley@gmail.com</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-btn
                    color="negative"
                    unelevated
                    class="text-dark text-capitalize"
                    text-color="dark"
                    style="width: 120px"
                    >Delete</q-btn
                  >
                </q-item-section>
              </q-item>
            </q-list>
            <q-separator class="q-my-lg" />
            <q-item-label header class="text-primary">
              View All Users
            </q-item-label>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-7">
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">Invite People</div>
            <q-separator class="q-my-lg" />

            <q-form>
              <div class="row q-col-gutter-md">
                <div class="col-10">
                  <q-input
                    dense
                    outlined
                    v-model="email"
                    placeholder="Email"
                    class="q-mb-md"
                    type="email"
                  />
                </div>
                <div class="col-2">
                  <q-btn
                    color="primary"
                    unelevated
                    class="text-dark text-capitalize full-width"
                    text-color="dark"
                    >Invite</q-btn
                  >
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
        <q-card flat class="bg-white q-mb-lg" style="border-radius: 16px">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">
              Create New Account
            </div>
            <q-separator class="q-my-lg" />

            <q-form>
              <div class="row">
                <div class="col-10">
                  <q-input
                    dense
                    outlined
                    v-model="projectName"
                    placeholder="User name"
                    class="q-mb-md"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="email"
                    placeholder="Email"
                    class="q-mb-md"
                    type="email"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="password"
                    placeholder="Password"
                    class="q-mb-md"
                    type="password"
                  />
                  <q-input
                    dense
                    outlined
                    v-model="confirmedPassword"
                    placeholder="Retype password"
                    class="q-mb-md"
                    type="password"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-md">
                <q-btn
                  color="primary"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="dark"
                  style="width: 204px"
                  >Sign Up</q-btn
                >
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
const projectName = ref("");
const email = ref("");
const password = ref("");
const confirmedPassword = ref("");
</script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}
.list-item {
  .q-item__label {
    font-style: normal;
    font-weight: 600;
    font-size: 19px;
    line-height: 19px;
  }
  .q-item__label--caption {
    font-style: normal;
    font-weight: 400;
    font-size: 17px;
    line-height: 21px;
    color: $dark-page;
  }
}
</style>
