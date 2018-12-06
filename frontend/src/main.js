// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import axios from 'axios'
import App from './App'
import router from './routes'
import axiosErrHandle from './utilities/axios-error-handler.js'

Vue.config.productionTip = false

// Do we have an existing session in sessionStorage (local storage API)
let token = sessionStorage.authToken
let auth = {
  authenticated: !!token,
  authToken: token || null
}
let clientOpts = {
  baseURL: '/api/',
  timeout: 5000
}
if (token) {
  clientOpts['headers'] = { 'Authorization': `Token ${token}` }
}

// Setup a rest api client
let client = axios.create(clientOpts)
// Handle various request error types in a uniform way.
client.interceptors.response.use(
  response => response, exc => axiosErrHandle(exc, router, auth)
)

// Prevent accessing routes that require authentication
router.beforeEach((to, from, next) => {
  if (!to.meta.public && !auth.authenticated) {
    next({ name: 'Login', query: { from: window.location.pathname } })
  }
  next()
})
window.vm = new Vue({
  el: '#app',
  router,
  data: {
    auth: auth,
    client
  },
  components: { App },
  template: '<App :auth="auth"/>'
})
