import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

import Sidebar from "./components/Sidebar.vue"
import Sorting from "./components/Sorting.vue"
import Pathfinding from "./components/Pathfinding.vue"

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons"

library.add(fas)

createApp(App)
    .use(router)
    .component("fas", FontAwesomeIcon)
    .component("Sorting", Sorting)
    .component("Pathfinding", Pathfinding)
    .component("Sidebar", Sidebar)

    .mount("#app")
