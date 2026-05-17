import { defineStore } from "pinia";
import { ref, watch } from "vue";

export type AuthTab = "login" | "register";

const STORAGE_KEY = "auth_tab";

function loadInitialTab(): AuthTab {
  const stored = sessionStorage.getItem(STORAGE_KEY);
  return stored === "register" ? "register" : "login";
}

export const useAuthStore = defineStore("auth", () => {
  const tab = ref<AuthTab>(loadInitialTab());

  watch(tab, (next) => {
    sessionStorage.setItem(STORAGE_KEY, next);
  });

  function setTab(value: AuthTab) {
    tab.value = value;
  }

  return { tab, setTab };
});
