import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { authGuard } from '@/guards/authGards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path:'/login',
      name:'login',
      component: () =>import('../views/LoginView.vue')
    },
    {
      path:'/registration',
      name:'registration',
      component: () => import('../views/RegistrationView.vue')
    },
    {
      path:'/dashboard',
      name:'dashboard',
      component: () => import('@/views/dashboarIndexView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/dashboard/customer/affairs',
      name:'affair',
      component: () => import('@/views/affairDashboard.vue'),
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
    }
  ],
})

export default router
