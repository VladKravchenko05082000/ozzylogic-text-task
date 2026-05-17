<script setup lang="ts">
import { useBreakpoint } from "@/composables/useBreakpoint";

import DesktopHeader from "./desktop/DesktopHeader.vue";
import MobileHeader from "./mobile/MobileHeader.vue";

import { mobileBreakPoint } from "@/configs/general-constants";

import { NavLinkItem } from "@/types/general-types";
import { useUserStore } from "@/stores/userStore";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const authStore = useAuthStore();

const router = useRouter();

const { isDesktop } = useBreakpoint(mobileBreakPoint);

const navLinks: NavLinkItem[] = [
  { to: "/rates", label: "Rates" },
  { to: "/banks", label: "Banks" },
  { to: "/nbu", label: "NBU" },
  { to: "/history", label: "History" },
  { to: "/branches", label: "Branches" },
];

async function handleLogout() {
  await authStore.logout();
  router.push("/");
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background">
    <header
      class="sticky top-0 z-30 border-b border-border bg-background/80 backdrop-blur"
      v-if="userStore.isAuthenticated"
    >
      <DesktopHeader :nav-links="navLinks" @logout="handleLogout" v-if="isDesktop" />
      <MobileHeader :nav-links="navLinks" @logout="handleLogout" v-else />
    </header>
    <main class="flex-1">
      <div class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-8">
        <slot />
      </div>
    </main>
  </div>
</template>
