import { computed, ref, watch } from "vue";
import { defineStore } from "pinia";

import { authApi } from "@/api/auth";

import { useUserStore } from "./userStore";

export type AuthTab = "login" | "register";

interface AuthDataPayloadInterface {
  email: string;
  password: string;
}

const STORAGE_KEY = "auth_tab";

function loadInitialTab(): AuthTab {
  const stored = sessionStorage.getItem(STORAGE_KEY);
  return stored === "register" ? "register" : "login";
}

export const useAuthStore = defineStore("auth", () => {
  const isLoading = ref(false);

  const tab = ref<AuthTab>(loadInitialTab());

  const hasAccessToken = computed(() => {
    return !!localStorage.getItem("access_token");
  });

  watch(tab, (next) => {
    sessionStorage.setItem(STORAGE_KEY, next);
  });

  function _saveTokens(tokens: { access_token: string; refresh_token: string }) {
    localStorage.setItem("access_token", tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
  }

  function clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  function setTab(value: AuthTab) {
    tab.value = value;
  }

  async function login(payload: AuthDataPayloadInterface) {
    const userStore = useUserStore();

    const { data } = await authApi.login(payload);

    _saveTokens(data.tokens);
    userStore.setUser(data.user);
  }

  async function register(payload: AuthDataPayloadInterface) {
    const userStore = useUserStore();

    const { data } = await authApi.register(payload);

    _saveTokens(data.tokens);
    userStore.setUser(data.user);
  }

  async function logout() {
    const userStore = useUserStore();

    const refresh = localStorage.getItem("refresh_token");

    try {
      if (refresh) {
        await authApi.logout(refresh);
      }
    } catch (_) {}

    clearTokens();
    userStore.clearUser();
  }

  return {
    isLoading,
    hasAccessToken,
    tab,
    clearTokens,
    setTab,
    login,
    register,
    logout,
  };
});
