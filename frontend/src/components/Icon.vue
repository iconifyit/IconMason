// eslint-disable-next-line
<template>
  <figure @click="openIconDetail">
    <div v-if="icon.svg_data" v-html="icon.svg_data"></div>
    <img v-if="!icon.svg_data" :src="icon.file" />
    <figcaption>{{icon.filetype}}</figcaption>
  </figure>
</template>

<script>
export default {
  name: 'Icon',
  props: ['icon'],
  methods: {
    openIconDetail () {
      this.$emit('openIconDetail', this.icon)
    }
  }
}
</script>
