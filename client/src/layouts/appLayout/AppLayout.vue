<script setup lang="ts">
import { ref } from "vue";

import { useBreakpoint } from "@/composables/useBreakpoint";

import DesktopHeader from "./desktop/DesktopHeader.vue";
import MobileHeader from "./mobile/MobileHeader.vue";

import { mobileBreakPoint } from "@/configs/general-constants";

import { NavLinkItem } from "@/types/types";

const { isDesktop } = useBreakpoint(mobileBreakPoint);
const isAuthenticated = ref<boolean>(true);

const navLinks: NavLinkItem[] = [
  { to: "/rates", label: "Курси" },
  { to: "/banks", label: "Банки" },
  { to: "/nbu", label: "НБУ" },
  { to: "/history", label: "Історія" },
  { to: "/branches", label: "Відділення" },
];
</script>

<template>
  <div class="min-h-screen flex flex-col bg-background">
    <header
      class="sticky top-0 z-30 border-b border-border bg-background/80 backdrop-blur"
      v-if="isAuthenticated"
    >
      <DesktopHeader :nav-links="navLinks" v-if="isDesktop" />
      <MobileHeader :nav-links="navLinks" v-else />
    </header>
    <main class="flex-1">
      <div class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-8">
        <slot />
      </div>
    </main>
  </div>
</template>
