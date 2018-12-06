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
      :iconData="iconData"
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
      iconData: [],
      sets: [],
      loading: false,
      currentGroupPath: [],
      currentSet: null,
      currentGroup: null,
      errors: [],
      modalActive: false,
      expandedNav: false,
      queryParams: {
        query: null,
        page: 1,
        group: null,
        iconset: null
      }
    }
  },
  methods: {
    setGroupEventHandler (paths) {
      let indexLastPath = -1
      if (this.currentGroupPath) {
        const lastPath = paths[paths.length - 1]
        indexLastPath = this.currentGroupPath.indexOf(lastPath)
      }
      if (indexLastPath > -1) {
        this.currentGroupPath = this.currentGroupPath.slice(0, indexLastPath)
        this.currentGroup = this.currentGroupPath[this.currentGroupPath.length - 1]
      } else {
        this.currentGroupPath = paths
        this.currentGroup = paths[paths.length - 1]
      }
      this.currentSet = null
      this.queryParams.iconset = null
      this.queryParams.page = 1
      this.queryParams.group = this.currentGroup ? this.currentGroup.uuid : null
      this.getSetsForQuery()
      this.getIconsForQuery()
    },
    setSetEventHandler (set) {
      if (this.currentSet === set) {
        this.currentSet = null
        this.queryParams.iconset = null
      } else {
        this.currentSet = set
        this.queryParams.iconset = set.uuid
      }
      this.queryParams.page = 1
      this.getIconsForQuery()
    },
    getIconsForQuery (add) {
      const comp = this
      const client = this.$root.client
      this.$emit('doLoading', true)
      const params = pickBy(this.queryParams, v => v)
      client.get('/icons/', { params })
        .then((response) => {
          if (add) {
            const iconData = comp.iconData
            iconData.next = response.data.next
            iconData.previous = response.data.previous
            iconData.results.push(...response.data.results)
            comp.iconData = iconData
          } else {
            comp.iconData = response.data
          }
        })
        .catch((exc) => {
          console.log(comp.errors)
          comp.errors.push(Object.values(exc.errors))
        })
        .then(() => {
          comp.$emit('doLoading', false)
        })
    },
    getSetsForQuery () {
      const comp = this
      const client = this.$root.client
      this.$emit('doLoading', true)
      const params = {
        group: this.currentGroup ? this.currentGroup.uuid : 'root'
      }
      client.get('/iconsets/', { params })
        .then(
          (response) => {
            comp.sets = response.data.results
          }
        )
        .catch((exc) => {
          console.log(comp.errors)
          comp.errors.push(Object.values(exc.errors))
        })
        .then(() => {
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
      this.queryParams.page = 1
      this.getIconsForQuery()
    }
  },
  mounted () {
    const comp = this
    const client = this.$root.client
    this.$emit('doLoading', true)
    client.get('/groups/')
      .then(
        (response) => {
          comp.groups = response.data.results
        }
      )
      .catch((exc) => {
        console.log(comp.errors)
        comp.errors.push(Object.values(exc.errors))
      })
      .then(() => {
        comp.$emit('doLoading', false)
      })
    this.getSetsForQuery()
    this.getIconsForQuery()
  }
}
</script>
