// import { getToken } from '@/utils/token'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Index',
    meta: {
      title: 'Home Page',
      keepAlive: true,
      requireAuth: false,
    },
    component: () => import('@/pages/Index.vue'),
  },
  {
    path: '/analysis',
    name: '上傳分析檔案',
    meta: {
      title: 'Analysis',
      keepAlive: true,
      requireAuth: false,
    },
    component: () => import('@/pages/BackendUploadPage/Index.vue'),
    children: [
      {
        path: ':hash',
        name: '上傳檔案分享',
        meta: {
          title: 'Analysis Result',
          keepAlive: true,
          requireAuth: false,
        },
        props: true,
        component: () => import('@/pages/BackendUploadPage/AnalysisResult.vue'),
      },
    ],
  },
  {
    path: '/frontend-analysis',
    name: '前端分析',
    meta: {
      title: 'Frontend Analysis',
      keepAlive: true,
      requireAuth: false,
    },
    component: () => import('@/pages/FrontendAnalysisPage/Index.vue'),
  },
  {
    path: '/risk-assessment',
    name: '風險評價計算',
    meta: {
      title: 'Risk Assessment',
      keepAlive: true,
      requireAuth: false,
    },
    component: () => import('@/pages/RiskAssessmentPage/Index.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from) => {
  console.log(to, from)
  // const token = getToken();
  // if (!token && to.name !== 'Index') {
  //     return { name: 'Index' };
  // }
})

export { router }
