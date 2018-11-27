// eslint-disable-next-line
<template>
  <div class="icon">
    <header>{{icon.name}}</header>
    <img :src="icon.file" />
    <footer>
      <Icon v-for="(tag, index) in icon.tags" :tag="tag" :key="index" />
    </footer>
  </div>
</template>

<script>
  import Tag from '@/components/Tag.vue'
  export default {
    name: 'Icon',
    props: ['icon'],
    components: { Tag }
  }
</script>
