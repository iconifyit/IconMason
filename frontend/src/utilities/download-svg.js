export default (iconData) => {
  let a = document.createElement('a')
  document.body.appendChild(a)
  a.style = 'display: none'
  let blob = new Blob([iconData.svg], {type: 'image/svg+xml;charset=utf-8'})
  let url = window.URL.createObjectURL(blob)
  a.href = url
  a.download = iconData.file
  a.click()
  window.URL.revokeObjectURL(url)
  a.parentNode.removeChild(a)
}
