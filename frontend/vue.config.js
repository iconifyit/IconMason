module.exports = {
  runtimeCompiler: true,
  devServer: {
    proxy: {
      '^/(api)|(admin)|(static/admin)|(static/rest_framework)': {
        target: 'http://localhost:9000'
      }
    }
  }
}
