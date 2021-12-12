import { createRouter, createWebHistory } from "vue-router"
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"
import Calculator from "../views/Calculator.vue"
import Registration from "../views/Registration.vue"

const routes = [
	{ path: "/", 				component: Home },
	{ path: "/login", 			component: Login },
	{ path: "/calculator", 		component: Calculator },
	{ path: "/registration", 	component: Registration }
]

const router = createRouter({
		history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
