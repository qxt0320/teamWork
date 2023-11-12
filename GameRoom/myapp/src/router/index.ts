import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/login/index.vue')
  },
  {
    path: '/gameroom',
    name: 'gameroom',
    component: () => import('../components/GameRoom.vue')
  },
  {
    path: '/createroom',
    name: 'createroom',
    component: () => import('../components/CreateRoom.vue')
  },
  {
    path: '/joinroom',
    name: 'joinroom',
    component: () => import('../components/JoinRoom.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
