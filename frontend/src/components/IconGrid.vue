// eslint-disable-next-line
<template>
  <section>
    <header>
      <h1>Icons</h1>
    </header>
    <Icon v-for="(icon, index) in icons" :icon="icon" :key="index" />
  </section>
</template>

<script>
import Icon from '@/components/Icon.vue'
export default {
  name: 'IconGrid',
  components: { Icon },
  props: ['icons'],
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>
