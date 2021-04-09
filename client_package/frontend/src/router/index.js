import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../App.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: App
  },
  {
    path: '/*',
    redirect: 'Home',
  }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
