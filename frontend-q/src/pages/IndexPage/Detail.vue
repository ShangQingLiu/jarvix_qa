<template>
  <div class="row">
    <div class="col-12">
      <q-card flat class="">
        <q-card-section>
          <div class="text-h6 text-weight-bold text-dark">Project Name</div>
          <q-separator class="q-my-lg" />
          <p class="text-dark-page">
            dolor in hendrerit in vulputate velit esse molestie consequat, vel
            illum dolore eu feugiat nulla facilisis at vero eros et accumsan et
            iusto odio dignissim dolor in hendrerit in vulputate velit esse
            molestie consequat, vel illum dolore eu feugiat nulla facilisis at
            vero eros et accumsan et iusto odio dignissim dolor in hendrerit in
            vulputate velit esse molestie consequat, vel illum dolore eu feugiat
            nulla facilisis at vero eros et accumsan et iusto odio dignissim
            dolor in hendrerit in vulputate velit esse molestie consequat, vel
            illum dolore eu feugiat nulla facilisis at vero eros et accumsan et
            iusto odio dignissim dolor in hendrerit in vulputate velit esse
            molestie consequat, vel illum dolore eu feugiat nulla facilisis at
            vero eros et accumsan et iusto odio dignissim
          </p>
          <q-separator class="q-my-lg" />
          <div class="q-my-md" style="height: 80px">
            <q-avatar
              v-for="n in 5"
              :key="n"
              size="50px"
              class="absolute"
              :style="`left: ${n * 40}px`"
            >
              <img :src="`https://cdn.quasar.dev/img/avatar${n + 1}.jpg`" />
            </q-avatar>
            <q-avatar
              color="primary"
              text-color="white"
              class="absolute numbered-avatar"
              size="54px"
              font-size="19px"
              :style="`left: ${6 * 40}px; border: 2px solid white;`"
            >
              <span>+3</span>
            </q-avatar>
          </div>
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              >Invite people</q-btn
            >
            <q-btn
              color="primary"
              unelevated
              class="text-capitalize"
              text-color="white"
              >Create New Project</q-btn
            >
            <q-btn
              color="dark1"
              unelevated
              class="text-capitalize"
              text-color="white"
              >Delete Project</q-btn
            >
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss">
.q-field--outlined .q-field__control:before {
  border: 0.4px solid $dark-page;
}

.numbered-avatar .q-avatar__content {
  width: 48px;
  height: 50px;
}
</style>
