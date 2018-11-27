// eslint-disable-next-line
<template>
  <section>
    <nav>
      <nav id="groups">
        <ul>
          <header>Groups</header>
          <GroupItem
              v-for="(group, index) in tree"
              :group="group"
              :key="index"
              :currentGroupPath="currentGroupPath"
              @setGroupEvent="setGroupEventHandler"
              :path="[group]"
          >
          </GroupItem>
        </ul>
      </nav>
      <nav id="sets" v-if="sets">
        <header>Sets</header>
        <SetItem
            v-for="set in sets"
            v-bind:set="set"
            v-bind:key="set.uuid"
            @setSet="setSetEventHandler"
            :currentSet="currentSet"
        >
        </SetItem>
      </nav>
    </nav>
    <main>
      <ErrorAlert :key="index" v-for="(index, error) in errors">{{error}}</ErrorAlert>
      <IconGrid :icons="icons"/>
    </main>
  </section>
</template>

<script>
import GroupItem from '@/components/GroupItem.vue'
import SetItem from '@/components/SetItem'
import ErrorAlert from '@/components/ErrorAlert'
import IconGrid from '@/components/IconGrid'
export default {
  name: 'Index',
  components: {
    GroupItem,
    SetItem,
    ErrorAlert,
    IconGrid
  },
  props: ['auth'],
  data () {
    return {
      tree: {},
      icons: [],
      sets: [],
      loading: false,
      currentGroupPath: [],
      currentSet: null,
      errors: {}
    }
  },
  methods: {
    setGroupEventHandler (paths) {
      this.currentGroupPath = paths
      let currentGroup = paths[paths.length - 1]
      this.sets = currentGroup.iconsets
      this.currentSet = null
      this.getIconsForNode(currentGroup)
    },
    setSetEventHandler (set) {
      this.currentSet = set
      this.getIconsForNode(set)
    },
    getIconsForNode (node) {
      let comp = this
      let client = this.$root.client
      this.$emit('doLoading', true)
      client.get('/icons/', {params: {node: node.uuid}})
        .then(
          function (response) {
            comp.icons = response.data.results
          },
          function (error) {
            if (error.response.status === 401) {
              comp.$emit('doLogout')
            }
          }
        )
        .catch(function (response) {
          comp.errors.push(response.data)
        })
        .then(function () {
          comp.$emit('doLoading', false)
        })
    }
  },
  mounted () {
    let comp = this
    let client = this.$root.client
    this.$emit('doLoading', true)
    client.get('/tree/')
      .then(
        function (response) {
          comp.tree = response.data.results
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
