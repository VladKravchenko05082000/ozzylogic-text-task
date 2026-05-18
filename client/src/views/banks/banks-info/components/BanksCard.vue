<script setup lang="ts">
interface Props {
  name: string;
  phone: string | null;
  logo: string | null;
  rating: number | null;
}

defineProps<Props>();
</script>

<template>
  <div class="flex items-start gap-3">
    <div
      v-if="logo"
      class="h-10 w-10 shrink-0 rounded-md bg-muted overflow-hidden flex items-center justify-center"
    >
      <img :src="logo" :alt="name" class="h-full w-full object-contain" />
    </div>
    <div class="flex-1 min-w-0">
      <h3 class="font-medium truncate">{{ name }}</h3>
      <p class="text-xs text-muted-foreground mt-0.5">
        {{ phone || "—" }}
      </p>
      <p v-if="rating" class="text-xs text-muted-foreground mt-1">Rating: {{ rating }}</p>
    </div>
  </div>
</template>
