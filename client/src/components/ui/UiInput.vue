<script setup lang="ts">
type InputType = "text" | "password" | "email" | "number" | "tel" | "url" | "search" | "date";

const props = defineProps<{
  modelValue?: string | number;
  type?: InputType;
  placeholder?: string;
  disabled?: boolean;
  label?: string;
  error?: string;
  step?: string | number;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <div class="space-y-1.5">
    <label v-if="props.label" class="text-sm font-medium text-foreground">{{ props.label }}</label>
    <input
      v-bind="props.modelValue !== undefined ? { value: props.modelValue } : {}"
      :type="props.type ?? 'text'"
      :placeholder="props.placeholder"
      :disabled="props.disabled"
      :step="props.step"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :class="[
        'flex h-9 w-full rounded-md border bg-background px-3 py-1 text-sm',
        'placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        'disabled:cursor-not-allowed disabled:opacity-50',
        props.error ? 'border-destructive' : 'border-input',
      ]"
    />
    <p v-if="props.error" class="text-xs text-destructive">{{ props.error }}</p>
  </div>
</template>
