// eslint-disable-next-line
<template>
  <nav class="main">
    <div class="title">
      <a href="/">IconViewer</a>
    </div>
    <a aria-expanded="false" class="vegan-burger sr-only" href="javascript:void(0);" role="button" tabindex="1">open the menu<span></span><span></span><span></span></a>
    <ul class="menu">
      <li><a href="//localhost:8080/api/">API</a></li>
      <li><a href="//localhost:8080/admin/">Admin</a></li>
      <li><router-link v-if="!auth.authenticated" to="/login">Login</router-link></li>
      <li><a href='#' v-if="auth.authenticated" @click="doLogout">Logout</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Nav',
  props: ['auth'],
  methods: {
    doLogout (event) {
      this.$emit('logout')
      event.target.closest('nav.main').classList.remove('responsive')
    }
  }

}
</script>
