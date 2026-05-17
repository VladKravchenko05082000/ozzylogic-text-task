<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="flex flex-col items-center justify-center py-24 text-center">
    <p class="text-xs uppercase tracking-wide text-muted-foreground">404</p>
    <h1 class="mt-2 text-xl font-semibold">Page not found</h1>
    <RouterLink to="/" class="mt-6 text-sm text-foreground underline-offset-4 hover:underline">
      Back to home
    </RouterLink>
  </div>
</template>
