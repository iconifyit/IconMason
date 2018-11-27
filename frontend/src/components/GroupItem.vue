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
        v-for="(subGroup, subIndex) in group.groups"
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
  methods: {
    setGroup (path) {
      this.$emit('setGroupEvent', path)
    }
  },
  computed: {
    hasGroups () {
      return this.group.groups &&
        this.group.groups.length
    },
    inPath () {
      return this.currentGroupPath.indexOf(this.group) > -1
    }
  }
}
</script>
