import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/dashboarIndexView.vue'),
    },
    {
      path:'/login',
      name:'login',
      component: () =>import('../views/LoginView.vue')
    },

    // About the dashboard
    {
      path:'/dashboard',
      name:'dashboard',
      component: () => import('@/views/mainDashboardIndex.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/affairs',
      name:'dashboard-affairs',
      component: () => import('@/views/dashboarIndexView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/recents',
      name:'dashboard-recents',
      component: () => import('@/views/recentsDashboard.vue')
    },
    {
      path:'/dashboard/customer/affairs',
      name:'affair',
      component: () => import('@/views/affairDashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/archives',
      name:'archives',
      component: () => import('@/views/dashboardArchiveView.vue')
    },
    {
      path:'/dashboard/charts',
      name:'charts',
      component: () => import('@/views/dashboardChart.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/customer-info',
      name:'customer-info',
      component: () => import('@/views/dashboardCustomerInfo.vue'),
      meta: { requiresAuth: true }
    },

    /* Register new customer, add folder affairs and add documents */
    {
      path:'/customer',
      name:'customer',
      component: () => import('@/components/section/newCustomer.vue'),
      meta: { requiresAuth: true }
    },

    {
      path:'/customer-list',
      name:'getCustomer',
      component:() => import('@/views/dashboarCustomer.vue')
    },

    {
      path:'/create-affairs',
      name:'create-affairs',
      component:() => import('@/components/section/affairCreationSection.vue')
    },

    {
      path:'/upload-file',
      name:'upload-file',
      component:() => import('@/components/section/uploadFileSection.vue')
    },

    /* About password reseting */

    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/views/passwordResetView.vue')
    }
  ],
})

export default router
