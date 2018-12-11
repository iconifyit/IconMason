// eslint-disable-next-line
<template>
  <div class="modal-wrapper" @click="closeIconDetail" @keyup.escape="closeIconDetail">
    <div class="modal">
      <header>
        <h5>{{icon.name}}</h5>
        <a class="close" href="#" @click="closeIconDetail">✖</a>
      </header>
      <main>
        <ErrorAlert
          :key="index"
          v-for="(index, error) in errors"
        >
          {{error}}
        </ErrorAlert>
        <article v-if="details">
          <table class="colorful">
            <thead>
              <tr><th colspan="2">Icon Details</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>Icon set:</td><td>{{details.icon_set.name}}</td>
              </tr>
              <tr v-if="details.icon_set.group">
                <td>Icon group:</td><td>{{details.icon_set.group.name}}</td>
              </tr>
              <tr>
                <td>File type:</td><td>{{details.filetype}}</td>
              </tr>
            </tbody>
          </table>
          <p v-if="details.svg_source" class="code-title">SVG Source</p>
          <div
            v-if="details.svg_source"
            class="source"
            v-html="details.svg_source"
          ></div>
          <div class="actions">
            <button
              v-if="details.svg_source"
              class="button good"
              @click="downloadSvg(icon.name+'.svg', icon.svg_data)"
            >
              Download
            </button>
            <a
              v-if="!details.svg_source"
              class="button good"
              :href="icon.file"
              :download="details.filename"
            >
              Download
            </a>
          </div>
        </article>
        <figure v-if="icon.svg_data" v-html="icon.svg_data"></figure>
        <figure v-if="!icon.svg_data">
          <img :src="icon.file" />
        </figure>
      </main>
      <footer>
        <div class="field small">
          <input
            type="text"
            id="tag"
            placeholder="Tag icon"
            @keyup.enter="addTag"
          />
        </div>
        <Tag v-for="(tag, index) in icon.tags" :tag="tag" :key="index" />
      </footer>
    </div>
    <Loading :loading="loading" />
  </div>
</template>

<script>
import Tag from '@/components/Tag'
import Loading from '@/components/Loading'
import ErrorAlert from '@/components/ErrorAlert'
import downloadSvg from '@/utilities/download-svg'
export default {
  name: 'IconDetail',
  props: ['icon'],
  components: { Tag, Loading, ErrorAlert },
  data () {
    return {
      loading: false,
      details: null,
      errors: {}
    }
  },
  methods: {
    closeIconDetail (event) {
      if (event && event.type === 'click' &&
            !event.target.classList.contains('close') &&
            !event.target.querySelector('.modal')) {
        return
      }
      this.$emit('closeIconDetail')
    },
    handleKeyUp (event) {
      if (event.keyCode === 27) {
        this.closeIconDetail()
      }
    },
    downloadSvg,
    addTag (event) {
      let comp = this
      let client = this.$root.client
      this.loading = true
      let data = { tags: [{ name: event.target.value }] }
      client.patch('/icons/' + this.icon.uuid + '/', data)
        .then(function (response) {
          comp.icon = response.data
        })
        .catch(function (exc) {
          comp.errors = exc.data
        })
        .then(function () {
          comp.loading = false
        })
    }
  },
  mounted: function () {
    let comp = this
    let client = this.$root.client
    this.loading = true
    client.get('/icons/' + this.icon.uuid + '/')
      .then(function (response) {
        comp.details = response.data
      })
      .catch(function (exc) {
        comp.errors = exc.data
      })
      .then(function () {
        comp.loading = false
      })
  },
  created: function () {
    document.addEventListener('keyup', this.handleKeyUp)
  },
  destroyed: function () {
    document.removeEventListener('keyup', this.handleKeyUp)
  }
}
</script>
