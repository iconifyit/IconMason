import isString from 'lodash/isString'
import debounce from 'lodash/debounce'

export default (el) => {
  // Responsive mode
  if (isString(el)) {
    el = document.querySelector(el)
  }
  let veganBurger = el.querySelector('a.vegan-burger')
  veganBurger.addEventListener('click', (event) => {
    el.classList.toggle('responsive')
  })
  // Close the responsive menu when it isn't required any more.
  window.addEventListener('resize', debounce(() => {
    if (getComputedStyle(veganBurger).display === 'none') {
      el.classList.remove('responsive')
    }
  }), 150)
}
