import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import Index from './components/NewIndex'
import VueDraggable from "vue-draggable";

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(VueDraggable);

const routes = [{
    path: '/scan_db',
    component: Index
  }, {
    path: '/sesam_response',
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