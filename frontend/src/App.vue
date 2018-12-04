// eslint-disable-next-line
<template>
  <section class="container">
    <header>
      <Nav :auth="auth" @logout="doLogout"/>
    </header>
    <router-view
      @login="doLogin"
      @doLoading="doLoading"
      :auth="auth"
    ></router-view>
    <Loading :loading="loading" />
  </section>
</template>
<script>
import responsiveNav from '@/utilities/navigation'
import Nav from '@/components/Nav'
import Loading from '@/components/Loading'
export default {
  name: 'app',
  props: ['auth'],
  data () {
    return {
      loading: false
    }
  },
  components: {
    Nav,
    Loading
  },
  mounted () {
    responsiveNav('nav.main')
  },
  methods: {
    doLogin (token) {
      this.auth.authenticated = true
      this.auth.authToken = token
      // Add the authorization token when we have it.
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
