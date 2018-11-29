// eslint-disable-next-line
<template>
  <li>
    <button
      @click='setGroup(path)'
      :class='{ active: inPath, more: hasGroups}'
    >
      {{group.name}}
    </button>
    <ul v-if="hasGroups && inPath">
      <GroupItem
        v-for="(subGroup, subIndex) in groups"
        :group="subGroup"
        :key="subIndex"
        :currentGroupPath="currentGroupPath"
        @setGroupEvent="setGroup([...path, subGroup])"
      ></GroupItem>
    </ul>
  </li>
</template>

<script>
export default {
  name: 'GroupItem',
  props: ['currentGroupPath', 'group', 'parent', 'path'],
  data () {
    return {
      groups: []
    }
  },
  methods: {
    setGroup (path) {
      this.$emit('setGroupEvent', path)
    }
  },
  computed: {
    hasGroups () {
      return this.group.groups && this.group.groups.length
    },
    inPath () {
      return this.currentGroupPath.indexOf(this.group) > -1
    }
  },
  mounted () {
    if (this.group.groups.length === 0)
      return
    let comp = this
    let client = this.$root.client
    this.$emit('doLoading', true)
    client.get('/groups/', {params: {group: this.group.uuid}})
      .then(
        function (response) {
          comp.groups = response.data.results
        }
      )
      .catch(function (response) {
        comp.errors.push(response.data)
      })
      .then(function () {
        comp.$emit('doLoading', false)
      })
  }
}
</script>
