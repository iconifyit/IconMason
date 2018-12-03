// eslint-disable-next-line
<template>
  <nav class="main">
    <div class="title">
      <a href="/">IconMason</a>
    </div>
    <a aria-expanded="false" class="vegan-burger sr-only" href="javascript:void(0);" role="button" tabindex="1">open the menu<span></span><span></span><span></span></a>
    <ul class="menu">
      <li class="dropdown">
        <a href="#" @click.prevent>Links</a>
        <ul>
          <li><a href="//localhost:8080/api/">API</a></li>
          <li><a href="//localhost:8080/admin/">Admin</a></li>
        </ul>
      </li>
      <li><router-link v-if="!auth.authenticated" to="/login">Login</router-link></li>
      <li><a href='#' v-if="auth.authenticated" @click="doLogout">Logout</a></li>
      <li>
        <button class="theme" @click="toggleTheme">
          <img :src="'/static/img/'+themeLink+'.svg'" />
        </button>
      </li>
      <li>
        <button :disabled="disableZoomIn" @click="zoomIn">
          <img :src="'/static/img/plus.svg#'+viewControl.theme" />
        </button>
      </li>
      <li>
        <button :disabled="disableZoomOut" @click="zoomOut">
          <img :src="'/static/img/minus.svg#'+viewControl.theme" />
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
import ViewControl from '@/utilities/view-control'
export default {
  name: 'Nav',
  props: ['auth'],
  data: function() {
    return {
      disableZoomIn: false,
      disableZoomOut: false,
      viewControl: null,
      themeLink: null
    }
  },
  methods: {
    doLogout (event) {
      this.$emit('logout')
      event.target.closest('nav.main').classList.remove('responsive')
    },
    toggleTheme () {
      [this.viewControl.theme, this.themeLink] = [
        this.themeLink, this.viewControl.theme
      ]
    },
    zoomIn () {
      let allowed = this.viewControl.zoom(1)
      this.disableZoomOut = false
      if (!allowed) {
        this.disableZoomIn = true
      }
    },
    zoomOut () {
      let allowed = this.viewControl.zoom(-1)
      this.disableZoomIn = false
      if (!allowed) {
        this.disableZoomOut = true
      }
    }
  },
  beforeMount () {
    this.viewControl = new ViewControl({
        zoomMin: 10,
        zoomMax: 22,
        useLocalStorage: true
    })
    this.themeLink = this.viewControl.theme === 'dark' ? 'light' : 'dark'
  }
}
</script>
