<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: { type: String, required: true },
});
</script>

<template>
  <div class="mb-6 sm:mb-8">
    <h1 class="text-xl sm:text-2xl font-semibold tracking-tight text-foreground">
      {{ title }}
    </h1>
    <p v-if="description" class="mt-1 text-sm text-muted-foreground">
      {{ description }}
    </p>
    <div v-if="$slots.actions" class="mt-4">
      <slot name="actions" />
    </div>
  </div>
</template>
