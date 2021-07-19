import Vue from 'vue'
import VueRouter from 'vue-router'
import page1 from '../components/page1.vue'
import page2 from '../components/page2.vue'
import page3 from '../components/page3.vue'
Vue.use(VueRouter)

const routes = [
  {
    path :'/page1',
    component : page1
  },
  {
    path :'/page2',
    component :page2,
  },
  {
    path :'/page3',
    component :page3,
  }
]

const router = new VueRouter({
    routes,
})

//导出
export default router
