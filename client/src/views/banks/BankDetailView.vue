<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";
import { useBanksStore } from "@/stores/banksStore";

const rateColumns: TableColumn[] = [
  { key: "currency", label: "Currency" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];
const route = useRoute();
const bankStore = useBanksStore();

onMounted(() => bankStore.fetchBank(route.params.slug as string));
</script>

<template>
  <div>
    <div v-if="bankStore.isLoading" class="space-y-4">
      <UiSkeleton class="h-24" />
      <UiSkeleton class="h-40" />
    </div>

    <div v-if="bankStore.currentBank && !bankStore.isLoading">
      <PageHeader
        :title="bankStore.currentBank.bank.name"
        :description="bankStore.currentBank.bank.description"
      />

      <!-- INFO -->
      <UiCard class="p-5 mb-6">
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <div>
            <dt class="text-xs text-muted-foreground">Website</dt>
            <dd class="mt-0.5">
              <a
                :href="bankStore.currentBank.bank.site"
                target="_blank"
                class="text-info hover:underline"
              >
                {{ bankStore.currentBank.bank.site }}
              </a>
            </dd>
          </div>
          <div>
            <dt class="text-xs text-muted-foreground">Phone</dt>
            <dd class="mt-0.5">{{ bankStore.currentBank.bank.phone || "—" }}</dd>
          </div>
          <div>
            <dt class="text-xs text-muted-foreground">Email</dt>
            <dd class="mt-0.5">{{ bankStore.currentBank.bank.email || "—" }}</dd>
          </div>
          <div>
            <dt class="text-xs text-muted-foreground">Rating</dt>
            <dd class="mt-0.5">{{ bankStore.currentBank.bank.rating || "—" }}</dd>
          </div>
          <div class="sm:col-span-2">
            <dt class="text-xs text-muted-foreground">Legal address</dt>
            <dd class="mt-0.5">{{ bankStore.currentBank.bank.legal_address || "—" }}</dd>
          </div>
        </dl>
      </UiCard>

      <!-- RATES -->
      <h2 class="text-sm font-semibold mb-3">Current rates</h2>
      <UiCard class="overflow-hidden mb-6">
        <UiTable
          v-if="bankStore.currentBank.rates.length"
          :columns="rateColumns"
          :rows="bankStore.currentBank.rates"
        >
          <template #cell-currency="{ row }">
            <UiBadge>{{ row.currency }}</UiBadge>
          </template>
          <template #cell-buy="{ row }">{{ row.buy.toFixed(2) }}</template>
          <template #cell-sell="{ row }">{{ row.sell.toFixed(2) }}</template>
        </UiTable>
        <p v-else class="p-4 text-sm text-muted-foreground">No rates available</p>
      </UiCard>

      <!-- BRANCHES -->
      <h2 class="text-sm font-semibold mb-3">
        Branches
        <span class="text-xs text-muted-foreground font-normal"
          >({{ bankStore.currentBank.branches.length }})</span
        >
      </h2>

      <div
        v-if="bankStore.currentBank.branches.length"
        class="grid grid-cols-1 md:grid-cols-2 gap-3"
      >
        <UiCard v-for="(br, i) in bankStore.currentBank.branches" :key="i" class="p-3">
          <div class="text-sm font-medium">{{ br.name || "Branch" }}</div>
          <div class="text-xs text-muted-foreground mt-1">{{ br.address }}</div>
          <div v-if="br.phone" class="text-xs text-muted-foreground mt-0.5">{{ br.phone }}</div>
        </UiCard>
      </div>
      <p v-else class="text-sm text-muted-foreground">No branches available</p>
    </div>
  </div>
</template>
