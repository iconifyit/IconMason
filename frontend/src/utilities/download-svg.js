export default (filename, iconData) => {
  let a = document.createElement('a')
  document.body.appendChild(a)
  a.style = 'display: none'
  let blob = new Blob([iconData], { type: 'image/svg+xml;charset=utf-8' })
  let url = URL.createObjectURL(blob)
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
  a.parentNode.removeChild(a)
}
