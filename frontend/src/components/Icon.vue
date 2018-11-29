// eslint-disable-next-line
<template>
  <figure @click="openIconDetail" v-html="icon.svg_data"></figure>
</template>

<script>
  import Tag from '@/components/Tag'
  export default {
    name: 'Icon',
    props: ['icon'],
    components: { Tag },
    methods: {
      openIconDetail () {
        this.$emit('openIconDetail', this.icon)
      }
    }
  }
</script>
