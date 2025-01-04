import { createRouter, createWebHistory } from 'vue-router'
import entrypoint from '@/components/entrypoint.vue'
import spotify_carthing from '@/components/spotify_carthing.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: entrypoint
    },
    {
      path: '/spotify_carthing',
      name: 'spotify_carthing',
      component: spotify_carthing
    }
  ]
})

export default router
