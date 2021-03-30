import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '../App.vue'
import PreferencesDialog from '../components/PreferencesDialog.vue'
import DatabaseOptionsPage from '../components/PreferencesDialog/DatabaseOptionsPage.vue'
import G2SpeechOptionsPage from '../components/PreferencesDialog/G2SpeechOptionsPage.vue'
import SubstitutionsOptionsPage from '../components/PreferencesDialog/SubstitutionsOptionsPage.vue'

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
        path: '/preferences/substitutions',
        component: SubstitutionsOptionsPage
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
