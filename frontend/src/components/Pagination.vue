// eslint-disable-next-line
<template>
  <nav class="pagination">
    <button @click="$emit('iconsAddBatch')" class="button" v-if="units.next">More..</button>
  </nav>
</template>

<script>
export default {
  name: 'Pagination',
  props: ['units'],
  data () {
    return {
    }
  },
  methods: { }
}
</script>
