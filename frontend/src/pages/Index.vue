// eslint-disable-next-line
<template>
  <section :class='{"modal-active": modalActive}'>
    <nav class="sidebar" :class="{expanded: expandedNav}">
      <button
        class="expand"
        :class="{expanded: expandedNav}"
        @click="toggleExpandedNav"
      >
        <div>❯❯</div>
      </button>
      <nav id="groups">
        <ul>
          <header>Groups</header>
          <GroupItem
              v-for="(group, index) in groups"
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
    <ErrorAlert
      :key="index"
      v-for="(index, error) in errors"
    >
      {{error}}
    </ErrorAlert>
    <IconGrid
      @modalState="modalState"
      @iconsAddBatch="iconsAddBatch"
      @doQuery="doQuery"
      :icon_data="icon_data"
    />
  </section>
</template>

<script>
import GroupItem from '@/components/GroupItem'
import SetItem from '@/components/SetItem'
import ErrorAlert from '@/components/ErrorAlert'
import IconGrid from '@/components/IconGrid'
import pickBy from 'lodash/pickBy'
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
      groups: [],
      icon_data: [],
      sets: [],
      loading: false,
      currentGroupPath: [],
      currentSet: null,
      errors: {},
      modalActive: false,
      expandedNav: false,
      queryParams: {
        query: null,
        page: 1,
        node: null
      }
    }
  },
  methods: {
    setGroupEventHandler (paths) {
      let currentGroup = null
      let indexLastPath = -1
      if (this.currentGroupPath) {
        let lastPath = paths[paths.length-1]
        indexLastPath = this.currentGroupPath.indexOf(lastPath)
      }
      if (indexLastPath > -1) {
        this.currentGroupPath = this.currentGroupPath.slice(0, indexLastPath)
        currentGroup = this.currentGroupPath[this.currentGroupPath.length - 1]
      } else {
        this.currentGroupPath = paths
        currentGroup = paths[paths.length - 1]
      }
      this.currentSet = null
      this.queryParams.page = 1
      this.queryParams.node = currentGroup ? currentGroup.uuid : null
      this.getIconsForQuery()
      if (!currentGroup || currentGroup.iconsets.length === 0) return
      let comp = this
      let client = this.$root.client
      this.$emit('doLoading', true)
      client.get('/iconsets/', {params: {group: currentGroup.uuid}})
        .then(
          function (response) {
            comp.sets = response.data.results
          }
        )
        .catch(function (response) {
          comp.errors.push(response.data)
        })
        .then(function () {
          comp.$emit('doLoading', false)
        })
    },
    setSetEventHandler (set) {
      if (this.currentSet == set) {
        this.currentSet = null
        this.queryParams.node = null
      } else {
        this.currentSet = set
        this.queryParams.node = set.uuid
      }
      this.queryParams.page = 1
      this.getIconsForQuery()
    },
    getIconsForQuery (add) {
      let comp = this
      let client = this.$root.client
      this.$emit('doLoading', true)
      let params = pickBy(this.queryParams, v=>v)
      client.get('/icons/', {params})
        .then(function (response) {
            if (add) {
              let icon_data = comp.icon_data
              icon_data.next = response.data.next
              icon_data.previous = response.data.previous
              icon_data.results.push(...response.data.results)
              comp.icon_data = icon_data
            } else {
              comp.icon_data = response.data
            }
        })
        .catch(function (response) {
          comp.errors.push(response.data)
        })
        .then(function () {
          comp.$emit('doLoading', false)
        })
    },
    iconsAddBatch () {
      this.queryParams.page = this.queryParams.page + 1
      this.getIconsForQuery(true)
    },
    modalState (state) {
      this.modalActive = state
    },
    toggleExpandedNav () {
      this.expandedNav = !this.expandedNav
    },
    doQuery (query) {
      this.queryParams.query = query
      this.getIconsForQuery()
    }
  },
  mounted () {
    let comp = this
    let client = this.$root.client
    this.$emit('doLoading', true)
    client.get('/groups/')
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
