import Vue from 'vue'
import Router from 'vue-router'
import Index from './views/Index'
import Login from './views/Login'

Vue.use(Router)

const router = new Router({
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
