<script setup lang="ts">
import { useRoute } from "vue-router";

import type { PropType } from "vue";
import { NavLinkItem } from "@/types/types";

defineProps({
  navLinks: { type: Array as PropType<NavLinkItem[]>, required: true },
});

const route = useRoute();

const isActive = (path: string) =>
  path === "/" ? route.path === "/" : route.path.startsWith(path);
</script>

<template>
  <div class="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
    <div class="flex items-center gap-8">
      <RouterLink to="/rates" class="text-sm font-semibold tracking-tight">Курси валют</RouterLink>

      <nav class="flex items-center gap-1">
        <RouterLink
          v-for="item in navLinks"
          :key="item.to"
          :to="item.to"
          :class="[
            'rounded-md px-3 py-1.5 text-sm transition-colors',
            isActive(item.to)
              ? 'bg-secondary text-foreground'
              : 'text-muted-foreground hover:bg-secondary/60 hover:text-foreground',
          ]"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </div>

    <div class="flex items-center gap-4">
      <RouterLink
        to="/profile"
        :class="[
          'rounded-md px-3 py-1.5 text-sm transition-colors',
          isActive('/profile')
            ? 'bg-secondary text-foreground'
            : 'text-muted-foreground hover:bg-secondary/60 hover:text-foreground',
        ]"
      >
        Profile
      </RouterLink>

      <button
        class="rounded-md px-3 py-1.5 text-sm text-destructive hover:text-foreground hover:bg-secondary/60 cursor-pointer"
      >
        Вийти
      </button>
    </div>
  </div>
</template>
