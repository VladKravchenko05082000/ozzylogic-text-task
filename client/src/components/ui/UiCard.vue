<script setup lang="ts">
defineProps({
  hoverable: Boolean,
});
</script>

<template>
  <div
    :class="[
      'rounded-lg border border-border bg-card text-card-foreground',
      hoverable && 'transition-colors hover:border-foreground/20 hover:bg-accent/40',
    ]"
  >
    <slot />
  </div>
</template>
