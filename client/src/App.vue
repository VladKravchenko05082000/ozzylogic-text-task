<script setup lang="ts">
import AuthLayout from "./layouts/AuthLayout.vue";
</script>

<template>
  <AuthLayout>
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </AuthLayout>
</template>
