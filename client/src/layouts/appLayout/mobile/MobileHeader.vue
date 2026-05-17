<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";

import BurgerMenuIcon from "@/components/icons/BurgerMenuIcon.vue";
import CloseIcon from "@/components/icons/CloseIcon.vue";

import type { PropType } from "vue";
import { NavLinkItem } from "@/types/general-types";

defineProps({
  navLinks: { type: Array as PropType<NavLinkItem[]>, required: true },
});

const emit = defineEmits<{ logout: [] }>();

const route = useRoute();
const open = ref(false);

const isActive = (path: string) =>
  path === "/" ? route.path === "/" : route.path.startsWith(path);

const close = () => {
  open.value = false;
};
</script>

<template>
  <div>
    <div class="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
      <RouterLink to="/rates" class="text-sm font-semibold tracking-tight"
        >Currency Rates</RouterLink
      >

      <button
        class="inline-flex h-9 w-9 items-center justify-center rounded-md hover:bg-secondary cursor-pointer"
        @click="open = !open"
        aria-label="menu"
      >
        <CloseIcon v-if="open" />
        <BurgerMenuIcon v-else />
      </button>
    </div>

    <div v-if="open" class="border-t border-border">
      <div class="mx-auto max-w-6xl px-4 py-3 space-y-1">
        <RouterLink
          v-for="item in navLinks"
          :key="item.to"
          :to="item.to"
          @click="close"
          :class="[
            'block rounded-md px-3 py-2 text-sm',
            isActive(item.to)
              ? 'bg-secondary text-foreground'
              : 'text-muted-foreground hover:bg-secondary/60',
          ]"
        >
          {{ item.label }}
        </RouterLink>

        <div class="border-t border-border pt-2 mt-2 space-y-1">
          <RouterLink
            to="/profile"
            @click="close"
            :class="[
              'block rounded-md px-3 py-2 text-sm',
              isActive('/profile')
                ? 'bg-secondary text-foreground'
                : 'text-muted-foreground hover:bg-secondary/60',
            ]"
          >
            Profile
          </RouterLink>

          <button
            class="w-full text-left rounded-md px-3 py-2 text-sm text-destructive cursor-pointer"
            @click="emit('logout')"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
