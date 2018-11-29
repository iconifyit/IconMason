<template>
  <div class="loading" v-if="loading">
    <div class="spinner"></div>
    Loading&#8230;
  </div>
</template>

<script>
export default {
  props: ['loading']
}
</script>
