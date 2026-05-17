import { useUserStore } from "@/stores/userStore";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "auth",
    component: () => import("@/views/auth/AuthView.vue"),
    meta: { title: "Auth", guestOnly: true },
  },
  {
    path: "/rates",
    name: "rates",
    component: () => import("@/views/rates/RatesView.vue"),
    meta: { title: "Rates", requiresAuth: true },
  },
  {
    path: "/banks",
    name: "banks",
    component: () => import("@/views/banks/BanksView.vue"),
    meta: { title: "Banks", requiresAuth: true },
  },
  {
    path: "/banks/:slug",
    name: "bank-detail",
    component: () => import("@/views/banks/BankDetailView.vue"),
    meta: { title: "Bank", requiresAuth: true },
  },
  {
    path: "/nbu",
    name: "nbu",
    component: () => import("@/views/nbu/NbuSummaryView.vue"),
    meta: { title: "NBU & Average", requiresAuth: true },
  },
  {
    path: "/history",
    name: "history",
    component: () => import("@/views/history/HistoryView.vue"),
    meta: { title: "Rate History", requiresAuth: true },
  },
  {
    path: "/branches",
    name: "branches",
    component: () => import("@/views/branches/BranchesView.vue"),
    meta: { title: "Branches", requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/views/profile/ProfileView.vue"),
    meta: { title: "Profile", requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/NotFoundView.vue"),
    meta: { title: "Not Found" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach(async (to) => {
  const userStore = useUserStore();

  if (!userStore.user && localStorage.getItem("access_token")) {
    await userStore.fetchMe();
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { name: "auth", query: { redirect: to.fullPath } };
  }

  if (to.meta.guestOnly && userStore.isAuthenticated) {
    return { name: "rates" };
  }
});

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title}` : "Fintracker";
});

export default router;
