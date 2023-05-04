<template>
  <div>
    <div class="row q-col-gutter-md">
      <UsersList />
      <div class="col-12 col-md-7">
        <q-card flat class="bg-white q-mb-lg">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">Invite People</div>
            <q-separator class="q-my-lg" />

            <q-form>
              <div class="row q-col-gutter-md">
                <div class="col-10">
                  <q-input
                    v-model="inviteEmail"
                    placeholder="Email"
                    class="q-mb-md"
                    type="email"
                    bg-color="accent"
                    :input-style="{ padding: '0px 23px' }"
                    borderless
                    dense
                  />
                </div>
                <div class="col-2">
                  <q-btn
                    color="primary"
                    unelevated
                    class="text-dark text-capitalize full-width"
                    text-color="white"
                    >Invite</q-btn
                  >
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
        <q-card flat class="bg-white q-mb-lg">
          <q-card-section>
            <div class="text-h6 text-weight-bold text-dark">
              Create New Account
            </div>
            <q-separator class="q-my-lg" />

            <q-form>
              <div class="row">
                <div class="col-10">
                  <q-input
                    v-model="username"
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
                  <q-input
                    v-model="password"
                    placeholder="Password"
                    class="q-mb-md"
                    bg-color="accent"
                    :input-style="{ padding: '0px 23px' }"
                    borderless
                    dense
                    type="password"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-md">
                <q-btn
                  color="primary"
                  unelevated
                  class="text-dark text-capitalize"
                  text-color="white"
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
import UsersList from "src/components/UserAuthenticationAndManagement/UsersList.vue";
import { ref } from "vue";

const username = ref("");
const email = ref("");
const password = ref("");
const inviteEmail = ref("");
</script>

<style lang="scss"></style>
