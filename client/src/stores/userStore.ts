import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { userApi } from "@/api/user";

import { useAuthStore } from "./authStore";

interface UserDataInterface {
  email: string;
  newsletter_enabled: boolean;
}

export interface ResetPasswordDataInterface {
  current_password: string;
  new_password: string;
}

interface UpdateUserDataResponseInterface {
  user: UserDataInterface;
}

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

  const error = ref<string | null>(null);

  async function updateProfile(payload: UserDataInterface) {
    isLoading.value = true;
    error.value = null;
    try {
      const { data }: { data: UpdateUserDataResponseInterface } =
        await userApi.updateProfile(payload);
      user.value = data.user;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
    } finally {
      isLoading.value = false;
    }
  }

  async function updatePassword(payload: ResetPasswordDataInterface) {
    isLoading.value = true;
    error.value = null;
    try {
      await userApi.changePassword(payload);
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
    } finally {
      isLoading.value = false;
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    setUser,
    clearUser,
    fetchMe,
    updateProfile,
    updatePassword,
  };
});
