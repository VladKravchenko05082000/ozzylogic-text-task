<script setup lang="ts">
import { useAuthStore } from "@/stores/authStore";
import UiTabSwitcher from "@/components/ui/UiTabSwitcher.vue";
import LoginForm from "../components/LoginForm.vue";
import RegisterForm from "../components/RegisterForm.vue";
import type { AuthTab } from "@/stores/authStore";

const auth = useAuthStore();

const authOptions: { value: AuthTab; label: string }[] = [
  { value: "login", label: "Login" },
  { value: "register", label: "Register" },
];
</script>

<template>
  <div class="px-4 py-8">
    <div class="mb-5 flex justify-center">
      <UiTabSwitcher
        :model-value="auth.tab"
        :options="authOptions"
        @update:model-value="auth.setTab"
      />
    </div>

    <h1 class="mb-5 text-center text-lg font-semibold tracking-tight">
      {{ auth.tab === "login" ? "Sign In" : "Create Account" }}
    </h1>

    <LoginForm v-if="auth.tab === 'login'" />
    <RegisterForm v-else />
  </div>
</template>
