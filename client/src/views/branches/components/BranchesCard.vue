<script setup lang="ts">
interface Props {
  bank_name: string;
  name: string;
  address: string;
  phone: string | null;
  distance_km: number;
}

defineProps<Props>();
</script>

<template>
  <div class="flex items-start justify-between gap-2">
    <div class="flex-1 min-w-0">
      <div class="text-sm font-medium truncate">{{ bank_name }}</div>
      <div class="text-xs text-muted-foreground mt-0.5">{{ name || "Branch" }}</div>
    </div>
    <span class="text-xs font-medium text-foreground tabular-nums">{{ distance_km }} km</span>
  </div>
  <div class="text-xs text-muted-foreground mt-2">{{ address }}</div>
  <div v-if="phone" class="text-xs text-muted-foreground mt-1">{{ phone }}</div>
</template>
