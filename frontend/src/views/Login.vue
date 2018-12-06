// eslint-disable-next-line
<template>
  <section>
    <form class="login" @submit.prevent="getAuthToken">
      <header><h2>Log In</h2></header>
      <ErrorAlert
        :key="index"
        v-for="(error, index) in errors.non_field_errors || [errors.detail]"
      >
        {{error}}
      </ErrorAlert>
      <main>
        <div class="field" :class="{bad: errors.username}">
          <label for="username">Username:</label>
          <input
            type="text"
            id="username"
            placeholder="Enter your username"
            v-model="credentials.username"
          >
          <span
            class="msg bad"
            :key="index"
            v-for="(error, index) in errors.username || {} "
          >
            {{error}}
          </span>
        </div>
        <div class="field" :class="{bad: errors.password}">
          <label for="password">Password:</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            v-model="credentials.password"
          >
          <span
            class="msg bad"
            :key="index"
            v-for="(error, index) in errors.password"
          >
            {{error}}
          </span>
        </div>
        <input :disabled="loginDisabled" class="button" type="submit" value="Login" />
      </main>
    </form>
  </section>
</template>

<script>
import ErrorAlert from '@/components/ErrorAlert'

export default {
  name: 'Login',
  props: ['auth'],
  data () {
    return {
      errors: {},
      credentials: {
        username: '',
        password: ''
      },
      loginDisabled: false
    }
  },
  components: {
    ErrorAlert
  },
  methods: {
    getAuthToken (username, password) {
      const comp = this
      const client = this.$root.client
      this.$emit('doLoading', true)
      this.lologinDisabled = true
      client.post(
        '/auth/', {
          username: this.credentials.username,
          password: this.credentials.password
        }
      )
        .then((response) => {
          comp.$emit('login', response.data.token)
        })
        .catch((exc) => {
          comp.errors = exc.errors
        }).then(() => {
          comp.credentials = {
            username: '',
            password: ''
          }
          comp.$emit('doLoading', false)
          this.loginDisabled = false
        })
    }
  }
}
</script>
