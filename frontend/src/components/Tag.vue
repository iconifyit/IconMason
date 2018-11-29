// eslint-disable-next-line
<template>
  <a class="tag" href="#">{{tag.name}}</a>
</template>

<script>
  export default {
    name: 'Tag',
    props: ['tag'],
  }
</script>
