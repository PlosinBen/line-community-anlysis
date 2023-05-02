<script lang="ts" setup>
// import { useTimeAgo } from '@vueuse/core'
import Header from '@/components/shared/Header.vue'
import Home from '@/pages/Index.vue'
// import Footer from '@/components/shared/Footer.vue'
// import { useUserStore } from '@/store/user'
// import ReloadPrompt from '@/pwa/ReloadPrompt.vue'
// import ServiceWorker from './components/ServiceWorker.vue'

// const userStore = useUserStore()

// userStore.initUser()

// const date = '__DATE__'
// const timeAgo = useTimeAgo(date)
</script>
<template>
  <!-- <div class="w-screen h-screen overflow-hidden flex flex-col">
    <div class="h-20">
      <Header />
    </div>
    <main class="grow overflow-hidden">
      <Home></Home>
    </main>
  </div> -->
  <el-container class="h-screen overflow-hidden">
    <el-header>
      <Header />
    </el-header>
    <el-main class="main overflow-hidden">
      <Home></Home>
      <!-- <RouterView /> -->
      <!-- <br />
      <ServiceWorker />
      <br />
      <div>Built at: {{ date }} ({{ timeAgo }})</div> -->
    </el-main>
    <!-- <el-footer>
      <Footer />
    </el-footer> -->
  </el-container>
  <!-- <ReloadPrompt /> -->
</template>
<style lang="scss">
#app {
  // font-family: Avenir, Helvetica, Arial, sans-serif;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  //   text-align: center;
  line-height: 150%;
}

.main {
  min-height: 500px;
}

.sw-msg {
  margin-top: 20px;
}
</style>
