import { isDark, toggleDark } from '@/composables'
// import { useDark, useToggle } from '@vueuse/core'

export function updateTheme() {
  if (isDark.value) {
    toggleDark()
  }
  // if (useDark()) {
  //   useToggle(useDark())
  // }
  // useDark()
}
