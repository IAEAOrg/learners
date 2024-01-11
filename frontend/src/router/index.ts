import { createRouter, createWebHistory } from "vue-router";
import { store } from "@/store";
import axios from "axios";
import { httpErrorHandler } from "@/helpers";
import Default from "@/layouts/default/Default.vue";
import Mainpage from "@/views/Mainpage.vue";
import Login from "@/views/Login.vue";
import Logout from "@/views/Logout.vue";

const routes = [
  {
    path: "/",
    component: Default,
    props: (route) => ({ routeHash: route.hash || "" }),
    children: [
      {
        path: "",
        name: "Mainpage",
        component: Mainpage,
      },
    ],
  },
  {
    path: "/login",
    component: Default,
    children: [
      {
        path: "",
        name: "Login",
        component: Login,
      },
    ],
  },
  {
    path: "/logout",
    component: Default,
    children: [
      {
        path: "",
        name: "Logout",
        component: Logout,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASEURL || "/"),
  linkActiveClass: "active",
  routes,
});

router.beforeEach(async (to) => {
  // No authorization on public pages
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);

  // Get authentication
  if (authRequired) {
    const authenticated = await IsAuthenticated();
    if (!authenticated) return "/login";
  }
});

function IsAuthenticated() {
  // Authenticate using the backend
  return axios
    .get("authentication")
    .then((response) => {
      store.dispatch("setError", "");
      return response.data.user;
    })
    .catch((error) => {
      httpErrorHandler(error);
      store.dispatch("resetTabs");
      return false;
    });
}

export default router;
