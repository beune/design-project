import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../App.vue'
import PreferencesDialog from '../components/PreferencesDialog.vue'
import DatabaseOptionsPage from '../components/PreferencesDialog/DatabaseOptionsPage.vue'
import G2SpeechOptionsPage from '../components/PreferencesDialog/G2SpeechOptionsPage.vue'
import SubstitutiesOptionsPage from '../components/PreferencesDialog/SubstitutiesOptionsPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: App
  },
  {
    path: '/preferences',
    component: PreferencesDialog,
    children: [
      {
        path: '/preferences/database',
        component: DatabaseOptionsPage
      },
      {
        path: '/preferences/g2speech',
        component: G2SpeechOptionsPage
      },
      {
        path: '/preferences/substituties',
        component: SubstitutiesOptionsPage
      },
      {
        path: '',
        redirect: 'database'
      },
      {
        path: '*',
        redirect: 'database'
      }
    ]
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
