import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import Index from './components/NewIndex'

Vue.config.productionTip = false

const routes = [{
    path: '/scan_db',
    component: Index
  }, {
    path: '/sesam_response',
    components: Index
  },
  {
    path: '/create_dataflow',
    components: Index
  },
  {
    path: '/connectors',
    components: Index
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
});