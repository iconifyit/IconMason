// eslint-disable-next-line
<template>
  <button @click='setSet(set)' :class='{ active: this.currentSet == set }'>
    {{ set.name }}
  </button>
</template>

<script>
export default {
  name: 'SetItem',
  props: ['sets']
}
</script>

<script>
export default {
  name: 'SetItem',
  props: ['currentSet', 'set'],
  methods: {
    setSet(event) {
      this.$emit('setSet', event)
    }
  }
}
</script>
