export default (exc, router, auth) => {
  let error
  if (typeof exc === 'object') {
    if (typeof exc.response !== 'undefined' &&
        typeof exc.response.data !== 'undefined') {
      if (exc.response.status === 401) {
        auth.authenticated = false
        auth.authToken = null
        router.push({ name: 'Login' })
      }
      error = new Error('Response error')
      error.errors = exc.response.data
      error.response = exc.response
      return Promise.reject(error)
    } else if (typeof exc.request !== 'undefined' &&
               typeof exc.request.status !== 'undefined') {
      let req = exc.request
      let status = req.status ? `${req.status}:` : ''
      error = new Error('Request error')
      error.errors = { 'non_field_errors': [
        `${status} ${req.statusText || req.responseText || exc.message}`
      ] }
      return Promise.reject(error)
    } else if (typeof exc.message !== 'undefined') {
      error = new Error('Request error')
      error.errors = { 'non_field_errors': [exc.message] }
      return Promise.reject(error)
    }
  }
  error = new Error('Unknown error')
  error.errors = { 'non_field_errors': [exc] }
  return Promise.reject(error)
}
