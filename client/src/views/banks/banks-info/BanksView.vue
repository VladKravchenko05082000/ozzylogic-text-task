<script setup lang="ts">
import { RouterLink } from "vue-router";
import { onMounted } from "vue";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";

import { useBanksStore } from "@/stores/banksStore";
import BanksCard from "./components/BanksCard.vue";

const bankStore = useBanksStore();

onMounted(() => bankStore.fetchBanks());
</script>

<template>
  <PageHeader title="Banks" description="5 banks supported by the service" />

  <div v-if="bankStore.isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
    <UiSkeleton v-for="i in 5" :key="i" class="h-24" />
  </div>

  <div v-if="bankStore.banks.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
    <RouterLink
      v-for="bank in bankStore.banks"
      :key="bank.slug"
      :to="`/banks/${bank.slug}`"
      class="block"
    >
      <UiCard hoverable class="p-4 h-full">
        <BanksCard :logo="bank.logo" :name="bank.name" :phone="bank.phone" :rating="bank.rating" />
      </UiCard>
    </RouterLink>
  </div>

  <UiEmpty v-else title="No banks found" />
</template>
