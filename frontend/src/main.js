// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import axios from 'axios'
import App from './App'
import router from './routes'

Vue.config.productionTip = false

// Do we have an existing session in sessionStorage (local storage API)
let token = sessionStorage.authToken
let auth = {
  authenticated: !!token,
  authToken: token || null
}
let clientOpts = {
  baseURL: process.env.API_URL,
  timeout: 5000
}
if (token) {
  clientOpts['headers'] = { 'Authorization': `Token ${token}` }
}

// Setup a rest api client
let client = axios.create(clientOpts)
// Handle various request error types in a uniform way.
client.interceptors.response.use(
  response => response,
  exc => {
    let error
    if (typeof exc.response !== 'undefined' &&
        typeof exc.response.data !== 'undefined') {
      if (error.response.status === 401) {
        auth.authenticated = false
        auth.authToken = null
        router.push({ name: 'Login' })
      }
      error = new Error('Response error')
      error.errors = exc.response.data
      error.response = exc.response
    } else if (typeof exc.request !== 'undefined' &&
               typeof exc.request.status !== 'undefined') {
      let req = exc.request
      let status = req.status ? `${req.status}:` : ''
      error = new Error('Request error')
      error.errors = { 'non_field_errors': [
        `${status} ${req.statusText || req.responseText || exc.message}`
      ] }
    } else if (typeof exc.message !== 'undefined') {
      error = new Error('Request error')
      error.errors = { 'non_field_errors': [exc.message] }
    } else {
      error = new Error('Unknown error')
      error.errors = { 'non_field_errors': [exc] }
    }
    return Promise.reject(error)
  }
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
