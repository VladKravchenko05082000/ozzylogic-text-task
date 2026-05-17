<script setup lang="ts">
import AppLayout from "./layouts/appLayout/AppLayout.vue";
</script>

<template>
  <AppLayout>
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </AppLayout>
</template>
