import Vue from 'vue';
import VueRouter from 'vue-router';
import ControlCenter from "../components/ControlCenter"
import DisplayRoom from "../components/DisplayRoom"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Control Center",
    component: ControlCenter
  },
  {
    path: "/display-room",
    name: "Display Room",
    component: DisplayRoom
  },
];

export const router = new VueRouter({
    mode:'history',
    routes,
});

// Setup beforeEach hook to check the logged in sync the loggin states with backend
router.beforeEach(async (to, from, next) => {
    next();
});

export default router;