// eslint-disable-next-line
<template>
  <main>
    <section class="grid">
      <SearchBar @doQuery="doQuery" />
      <Icon
        v-for="(icon, index) in iconData.results"
        :icon="icon"
        :key="index"
        @openIconDetail="openIconDetail"
      />
    </section>
    <Pagination :units="iconData" @iconsAddBatch="$emit('iconsAddBatch')" />
    <IconDetail
      v-if="selectedIcon"
      :icon="selectedIcon"
      @closeIconDetail="closeIconDetail"
    />
  </main>
</template>

<script>
import Icon from '@/components/Icon'
import IconDetail from '@/components/IconDetail'
import Pagination from '@/components/Pagination'
import SearchBar from '@/components/SearchBar'
export default {
  name: 'IconGrid',
  components: { Icon, IconDetail, Pagination, SearchBar },
  props: ['iconData'],
  data () {
    return {
      selectedIcon: null
    }
  },
  methods: {
    openIconDetail (icon) {
      this.$emit('modalState', true)
      this.selectedIcon = icon
    },
    closeIconDetail () {
      this.$emit('modalState', false)
      this.selectedIcon = null
    },
    doQuery (query) {
      this.$emit('doQuery', query)
    }
  }
}
</script>
