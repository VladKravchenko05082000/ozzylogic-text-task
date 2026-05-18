<script setup lang="ts">
interface Props {
  site: string;
  phone: string | null;
  email: string | null;
  rating: number | null;
  legal_address: string | null;
}

defineProps<Props>();
</script>

<template>
  <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
    <div>
      <dt class="text-xs text-muted-foreground">Website</dt>
      <dd class="mt-0.5">
        <a :href="site" target="_blank" class="text-info hover:underline">
          {{ site }}
        </a>
      </dd>
    </div>
    <div>
      <dt class="text-xs text-muted-foreground">Phone</dt>
      <dd class="mt-0.5">{{ phone || "—" }}</dd>
    </div>
    <div>
      <dt class="text-xs text-muted-foreground">Email</dt>
      <dd class="mt-0.5">{{ email || "—" }}</dd>
    </div>
    <div>
      <dt class="text-xs text-muted-foreground">Rating</dt>
      <dd class="mt-0.5">{{ rating || "—" }}</dd>
    </div>
    <div class="sm:col-span-2">
      <dt class="text-xs text-muted-foreground">Legal address</dt>
      <dd class="mt-0.5">{{ legal_address || "—" }}</dd>
    </div>
  </dl>
</template>
