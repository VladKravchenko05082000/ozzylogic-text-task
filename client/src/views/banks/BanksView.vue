<script setup lang="ts">
import { RouterLink } from "vue-router";
import { onMounted } from "vue";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";

import { useBanksStore } from "@/stores/banksStore";

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
        <div class="flex items-start gap-3">
          <div
            v-if="bank.logo"
            class="h-10 w-10 shrink-0 rounded-md bg-muted overflow-hidden flex items-center justify-center"
          >
            <img :src="bank.logo" :alt="bank.name" class="h-full w-full object-contain" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-medium truncate">{{ bank.name }}</h3>
            <p class="text-xs text-muted-foreground mt-0.5">
              {{ bank.phone || "—" }}
            </p>
            <p v-if="bank.rating" class="text-xs text-muted-foreground mt-1">
              Rating: {{ bank.rating }}
            </p>
          </div>
        </div>
      </UiCard>
    </RouterLink>
  </div>

  <UiEmpty v-else title="No banks found" />
</template>
