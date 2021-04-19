import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "@/components/Login"
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  }
]

const router = new VueRouter({
  routes
})

export default router
