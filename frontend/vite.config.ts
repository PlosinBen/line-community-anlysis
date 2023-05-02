import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import * as path from 'path'
// import { ManifestOptions, VitePWA, VitePWAOptions } from 'vite-plugin-pwa'
import replace from '@rollup/plugin-replace'
import { createHtmlPlugin } from 'vite-plugin-html'
// import VueI18n from '@intlify/unplugin-vue-i18n/vite'
import Unocss from 'unocss/vite'

// const pwaOptions: Partial<VitePWAOptions> = {
//   mode: 'development',
//   base: '/',
//   includeAssets: ['favicon.svg'],
//   manifest: {
//     name: 'PWA Router',
//     short_name: 'PWA Router',
//     theme_color: '#ffffff',
//     icons: [
//       {
//         src: 'pwa-192x192.png', // <== don't add slash, for testing
//         sizes: '192x192',
//         type: 'image/png',
//       },
//       {
//         src: '/pwa-512x512.png', // <== don't remove slash, for testing
//         sizes: '512x512',
//         type: 'image/png',
//       },
//       {
//         src: 'pwa-512x512.png', // <== don't add slash, for testing
//         sizes: '512x512',
//         type: 'image/png',
//         purpose: 'any maskable',
//       },
//     ],
//   },
//   devOptions: {
//     enabled: process.env.SW_DEV === 'true',
//     /* when using generateSW the PWA plugin will switch to classic */
//     type: 'module',
//     navigateFallback: 'index.html',
//   },
// }

// const claims = process.env.CLAIMS === 'true'
const reload = process.env.RELOAD_SW === 'true'

// if (process.env.SW === 'true') {
//   pwaOptions.srcDir = 'src'
//   pwaOptions.filename = claims ? 'claims-sw.ts' : 'prompt-sw.ts'
//   pwaOptions.strategies = 'injectManifest'
//   ;(pwaOptions.manifest as Partial<ManifestOptions>).name = 'PWA Inject Manifest'
//   ;(pwaOptions.manifest as Partial<ManifestOptions>).short_name = 'PWA Inject'
// }

// if (claims) pwaOptions.registerType = 'autoUpdate'
const title = '資工世紀帝國探吉教 LINE 群組訊息分析'
// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData: `@use "@/assets/styles/element/index.scss" as *;`,
      },
    },
  },
  plugins: [
    vue(),
    createHtmlPlugin({
      minify: true,
      /**
       * Data that needs to be injected into the index.html ejs template
       */
      inject: {
        data: {
          title,
        },
      },
    }),
    AutoImport({
      imports: ['vue', 'vue-router', 'vue-i18n', 'vue/macros', '@vueuse/head', '@vueuse/core'],
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),

    // https://github.com/antfu/unocss
    // see unocss.config.ts for config
    Unocss(),

    // VitePWA(pwaOptions),

    // https://github.com/intlify/bundle-tools/tree/main/packages/unplugin-vue-i18n
    // VueI18n({
    //   runtimeOnly: true,
    //   compositionOnly: true,
    //   fullInstall: true,
    //   include: [path.resolve(__dirname, 'locales/**')],
    // }),

    replace({
      preventAssignment: true,
      __DATE__: new Date().toISOString(),
      __RELOAD_SW__: reload ? 'true' : '',
      __TITLE__: title,
    }),
  ],
  server: {
    port: 8080,
    hmr: {
      path: "/socket",
      port: 8888,
      clientPort: 8080
    },
  },
})
