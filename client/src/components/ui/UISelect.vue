<script setup lang="ts">
interface Option {
  label: string;
  value: string;
}

const props = defineProps<{
  modelValue?: string;
  options: Option[];
  label?: string;
  error?: string;
  disabled?: boolean;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <div class="space-y-1.5">
    <label v-if="props.label" class="text-sm font-medium text-foreground">{{ props.label }}</label>
    <select
      :value="props.modelValue"
      :disabled="props.disabled"
      @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      :class="[
        'flex h-9 w-full rounded-md border bg-background px-3 text-sm',
        'focus:outline-none focus:ring-2 focus:ring-ring',
        'disabled:cursor-not-allowed disabled:opacity-50',
        props.error ? 'border-destructive' : 'border-input',
      ]"
    >
      <option v-for="option in props.options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <p v-if="props.error" class="text-xs text-destructive">{{ props.error }}</p>
  </div>
</template>
