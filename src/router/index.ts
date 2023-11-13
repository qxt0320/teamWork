import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/login/index.vue')
  },
  {
    path: '/menu',
    name: 'menu',
    component: () => import('../components/Menu.vue')
  },
  {
    path: '/guide',
    name: 'guide',
    component: () => import('../components/Guide.vue')
  },
  {
    path: '/gamestart',
    name: 'gamestart',
    component: () => import('../components/GameStart.vue')
  },
   {
  path: '/shouye',
  name: 'shouye',
  component: () => import('../components/ShouYe.vue')
},
{
  path: '/zhuce',
  name: 'zhuce',
  component: () => import('../components/ZhuCe.vue')
},
{
  path: '/succeedpage',
  name: 'succeedpage',
  component: () => import('../components/SucceedPage.vue')
},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
