// eslint-disable-next-line
<template>
  <div class="container">
    <header>
      <Nav :auth="auth" @logout="doLogout"/>
    </header>
    <router-view
      @login="doLogin"
      @doLoading="doLoading"
      :auth="auth"
    ></router-view>
    <div class="loading" v-if="loading===true">
      <div class="spinner"></div>
      Loading&#8230;
    </div>
  </div>
</template>
<script>
import responsiveNav from '@/navigation'
import Nav from '@/components/nav'
export default {
  name: 'app',
  props: ['auth'],
  data () {
    return {
      loading: false
    }
  },
  components: {
    Nav
  },
  mounted () {
    responsiveNav('nav.main')
  },
  methods: {
    doLogin (token) {
      this.auth.authenticated = true
      this.auth.authToken = token
      console.log(this.$root.client)
      this.$root.client.defaults.headers.common['Authorization'] = `Token: $(token)`
      sessionStorage.authToken = token
      this.$router.push(this.$route.query.from || '/')
    },
    doLogout () {
      this.auth.authenticated = false
      this.auth.authToken = null
      this.$router.push({name: 'Login'})
    },
    doLoading (state) {
      this.loading = state
    }
  }
}
</script>
<style src="./assets/sass/app.scss" lang="scss"></style>
