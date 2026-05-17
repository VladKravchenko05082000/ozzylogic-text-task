<script setup lang="ts">
import { useBreakpoint } from "@/composables/useBreakpoint";
import AuthDesktop from "./desktop/AuthDesktop.vue";
import AuthMobile from "./mobile/AuthMobile.vue";

const { isDesktop } = useBreakpoint(768);
</script>

<template>
  <AuthDesktop v-if="isDesktop" />
  <AuthMobile v-else />
</template>
