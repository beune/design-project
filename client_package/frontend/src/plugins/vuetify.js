import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

const opts = {}

export default new Vuetify({
  opts,
  theme: {
    themes: {
      light: {
        primary: '#1976d2',
      },
      dark:{
        primary: '#1976d2',
    }
    },
  },
})
