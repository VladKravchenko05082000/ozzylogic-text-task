<script setup lang="ts">
defineProps({
  title: { type: String, default: "Нічого не знайдено" },
  description: String,
});
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 text-center">
    <h3 class="text-sm font-medium text-foreground">{{ title }}</h3>
    <p v-if="description" class="mt-1 text-sm text-muted-foreground">{{ description }}</p>
    <slot />
  </div>
</template>
