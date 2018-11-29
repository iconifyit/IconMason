// eslint-disable-next-line
<template>
  <div class="search field">
    <label for="search">
      Search:
      <input
        name="search"
        id="search"
        @input="doQuery"
        @keyup.enter="flushQuery"
        @keyup.escape="cancelQuery"
        type="text"
      />
    </label>
  </div>
</template>

<script>
  import debounce from 'lodash/debounce'
  export default {
    name: 'SearchBar',
    data () {
      return {
        cancel: null,
        flush: null
      }
    },
    methods: {
      doQuery (event) {
        let vm = this
        let query = event.target.value
        this.cancelQuery()
        let debouncedQuery = debounce(() => {
          vm.$emit("doQuery", query)
        }, 1000)
        this.cancel = debouncedQuery.cancel
        this.flush = debouncedQuery.flush
        debouncedQuery()
      },
      cancelQuery () {
        if (this.cancel) {
          this.cancel()
          console.log("cancel!")
        }
      },
      flushQuery () {
        if (this.flush) {
          this.flush()
          console.log("flush!")
        }
      }
    }
  }
</script>
