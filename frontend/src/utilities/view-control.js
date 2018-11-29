class ViewControl {
  constructor (options) {
    Object.assign(this, this.defaults, options)
    let fontSize, theme
    if (this.useLocalStorage) {
      fontSize = localStorage.getItem('fontSize')
      theme = localStorage.getItem('theme')
    }
    if (!fontSize) {
      fontSize = this.fontSizeFromHtml
    }
    if (!theme) {
      theme = this.html.getAttribute('theme') || undefined
    }
    this.setFontSize(fontSize)
    if (typeof theme === 'string' && theme.length > 0) {
      this.theme = theme
    }
  }

  changeFontSize (add) {
    return this.setFontSize(parseInt(this.fontSize) + add)
  }

  zoom () {
    return this.changeFontSize(...arguments)
  }

  setFontSize (fontSize) {
    fontSize = parseInt(fontSize)
    if ((this.zoomMin > fontSize || fontSize > this.zoomMax)) return false
    this.fontSize = fontSize
    this.html.style.fontSize = fontSize + 'px'
    if (this.useLocalStorage) {
      localStorage.setItem('fontSize', fontSize)
    }
    return true
  }

  get html () {
    if (!this._html) {
      this._html = document.getElementsByTagName('html')[0]
    }
    if (this._html.nodeName && this._html.nodeName === 'HTML') {
      return this._html
    }
    throw new Error('HTML element not found, DOM not ready?')
  }

  get fontSizeFromHtml () {
    return parseInt(getComputedStyle(this.html).fontSize.replace(/px$/, ''))
  }

  get theme () {
    return this._theme
  }

  set theme (theme) {
    this._theme = theme
    if (this.useLocalStorage) {
      localStorage.setItem('theme', theme)
    }
    this.html.setAttribute('theme', theme)
  }
}

ViewControl.prototype.defaults = {
  min: 8,
  max: 32,
  useLocalStorage: true
}

export default ViewControl
