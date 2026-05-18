<script setup lang="ts">
interface Props {
  name: string;
  address: string;
  phone?: string;
}

defineProps<Props>();
</script>

<template>
  <div class="text-sm font-medium">{{ name || "Branch" }}</div>
  <div class="text-xs text-muted-foreground mt-1">{{ address }}</div>
  <div v-if="phone" class="text-xs text-muted-foreground mt-0.5">{{ phone }}</div>
</template>
