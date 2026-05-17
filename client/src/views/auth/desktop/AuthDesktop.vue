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
  <div class="flex min-h-[calc(100vh-7rem)] items-center justify-center px-6 py-12">
    <div class="w-full max-w-md">
      <div class="mb-6 flex justify-center">
        <UiTabSwitcher
          :model-value="auth.tab"
          :options="authOptions"
          @update:model-value="auth.setTab"
        />
      </div>

      <div class="rounded-lg border border-border bg-card p-6">
        <h1 class="mb-6 text-xl font-semibold tracking-tight">
          {{ auth.tab === "login" ? "Sign In" : "Create Account" }}
        </h1>

        <LoginForm v-if="auth.tab === 'login'" />
        <RegisterForm v-else />
      </div>
    </div>
  </div>
</template>
