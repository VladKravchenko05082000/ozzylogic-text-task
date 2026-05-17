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
    meta: { title: "Курси" },
  },
  {
    path: "/banks",
    name: "banks",
    component: () => import("@/views/banks/BanksView.vue"),
    meta: { title: "Банки" },
  },
  {
    path: "/banks/:slug",
    name: "bank-detail",
    component: () => import("@/views/banks/BankDetailView.vue"),
    meta: { title: "Банк" },
  },
  {
    path: "/nbu",
    name: "nbu",
    component: () => import("@/views/nbu/NbuSummaryView.vue"),
    meta: { title: "НБУ і середнє" },
  },
  {
    path: "/history",
    name: "history",
    component: () => import("@/views/history/HistoryView.vue"),
    meta: { title: "Історія курсів" },
  },
  {
    path: "/branches",
    name: "branches",
    component: () => import("@/views/branches/BranchesView.vue"),
    meta: { title: "Відділення" },
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/views/profile/ProfileView.vue"),
    meta: { title: "Профіль", requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/NotFoundView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
