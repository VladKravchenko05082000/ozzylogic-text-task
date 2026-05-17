<script setup lang="ts">
type Variant = "default" | "success" | "warning" | "destructive" | "info";

const props = defineProps<{
  variant?: Variant;
}>();

const variants: Record<Variant, string> = {
  default: "bg-secondary text-secondary-foreground",
  success: "bg-success-muted text-success",
  warning: "bg-warning-muted text-warning-foreground",
  destructive: "bg-destructive-muted text-destructive",
  info: "bg-info-muted text-info",
};
</script>

<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
      variants[props.variant ?? 'default'],
    ]"
  >
    <slot />
  </span>
</template>
