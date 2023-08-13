<template>
  <q-item class="q-mb-md" clickable :to="link">
    <q-item-section v-if="icon" avatar>
      <q-icon size="30px" :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-white">{{
        $t(`MainLayout.links.${title}`)
      }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'EssentialLink',
  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: '',
    },

    link: {
      type: String,
      default: '#',
    },

    icon: {
      type: String,
      default: '',
    },
  },
});
</script>

<style lang="scss" scoped>
.q-item {
  // border-radius: 12px 0px 0px 12px;
}
.q-item__label {
  font-style: normal;
  font-weight: 400;
  font-size: 19px;
  line-height: 28px;
}

</style>
