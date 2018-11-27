import Vue from 'vue'
import Router from 'vue-router'
import Index from './pages/Index'
import Login from './pages/Login'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Index
    }, {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { public: true }
    }
  ]
})

export default router
