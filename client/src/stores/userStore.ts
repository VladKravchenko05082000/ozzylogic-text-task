import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { userApi } from "@/api/user";

import { useAuthStore } from "./authStore";

interface UserDataInterface {
  email: string;
  newsletter_enabled: boolean;
}

interface UpdateUserDataPayloadInterface extends UserDataInterface {}

export const useUserStore = defineStore("user", () => {
  const user = ref<UserDataInterface | null>(null);
  const isLoading = ref(false);

  const isAuthenticated = computed(() => !!user.value);

  function setUser(payload: UserDataInterface) {
    user.value = payload;
  }

  function clearUser() {
    user.value = null;
  }

  async function fetchMe() {
    const authStore = useAuthStore();

    if (!localStorage.getItem("access_token")) {
      return;
    }

    try {
      const { data } = await userApi.me();

      user.value = data.user;
    } catch (_) {
      clearUser();
      authStore.clearTokens();
    }
  }

  async function updateProfile(payload: UpdateUserDataPayloadInterface) {
    const { data } = await userApi.updateProfile(payload);

    user.value = data.user;
  }

  return {
    user,
    isLoading,
    isAuthenticated,
    setUser,
    clearUser,
    fetchMe,
    updateProfile,
  };
});
