import Vue from 'vue'
import App from './App.vue'
import router from './router'

// TODO optimize imports: https://vuematerial.io/getting-started/
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'


// https://github.com/vuematerial/vue-material/issues/2285#issuecomment-769174375
Vue.config.errorHandler = (err) => {
  // Show any error but this one
  if (err.message !== "can't access property \"badInput\", this.$el.validity is undefined") {
    console.error(err);
  }
};

Vue.use(VueMaterial)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
