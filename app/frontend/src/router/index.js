import Vue from 'vue'
import Router from 'vue-router'
import Helloworld from '@/pages/Helloworld'

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/hello',
        name: 'Helloworld',
        component: Helloworld,
    }]
})