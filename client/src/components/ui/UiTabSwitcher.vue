<script setup lang="ts" generic="T extends string">
defineProps<{
  modelValue: T;
  options: { value: T; label: string }[];
}>();

defineEmits<{
  (e: "update:modelValue", value: T): void;
}>();
</script>

<template>
  <div class="inline-flex items-center rounded-md bg-secondary p-1">
    <button
      v-for="opt in options"
      :key="opt.value"
      type="button"
      @click="$emit('update:modelValue', opt.value)"
      :class="[
        'rounded-md px-4 py-1.5 text-sm font-medium transition-colors cursor-pointer',
        modelValue === opt.value
          ? 'bg-background text-foreground shadow-sm'
          : 'text-muted-foreground hover:text-foreground',
      ]"
    >
      {{ opt.label }}
    </button>
  </div>
</template>
