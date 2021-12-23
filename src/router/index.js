import { createRouter, createWebHistory } from "vue-router"
import Home from "../views/Home.vue"
import Login from "../views/Login.vue"
import Registration from "../views/Registration.vue"

import ProjectOverview from "../views/ProjectOverview.vue"
import Visualizer from "../views/Projects/Visualizer.vue"

import PageNotFound from "../views/PageNotFound.vue"

const routes = [
	{ path: "/", 						component: Home },
	{ path: "/login", 					component: Login },
	{ path: "/registration", 			component: Registration },
	{ path: "/projects", 				component: ProjectOverview },
	{ path: "/projects/sorting", 		component: Visualizer },
	{ path: "/projects/pathfinding", 	component: Visualizer },
	
	{ path: "/:catchAll(.*)*",  		component: PageNotFound }
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
})

export default router
