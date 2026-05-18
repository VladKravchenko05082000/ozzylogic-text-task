<script setup lang="ts">
import { computed, onMounted } from "vue";

import { useBanksStore } from "@/stores/banksStore";
import { useCurrencyStore } from "@/stores/currencyStore";
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";
import RatesFiltersSection from "./components/RatesFiltersSection.vue";

const banksStore = useBanksStore();
const currencyStore = useCurrencyStore();

const bankMap = computed(() =>
  Object.fromEntries(banksStore.banks.map((bank) => [bank.slug, bank])),
);

const ratesColumns: TableColumn[] = [
  { key: "bank_slug", label: "Bank", tdClass: "font-medium" },
  { key: "currency", label: "Currency" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];

onMounted(async () => {
  const promises: Promise<unknown>[] = [
    banksStore.fetchBanks(),
    currencyStore.fetchCurrencies(),
  ];
  if (!currencyStore.rates.length) {
    promises.push(
      currencyStore.fetchRates({
        banks: currencyStore.selectedBanks,
        currencies: currencyStore.selectedCurrencies,
      }),
    );
  }
  await Promise.all(promises);
});
</script>

<template>
  <PageHeader title="Exchange Rates" description="Current buy and sell rates across all banks" />

  <UiCard class="mb-6 p-4 sm:p-5">
    <RatesFiltersSection />
  </UiCard>

  <div v-if="currencyStore.isLoading" class="space-y-2">
    <UiSkeleton v-for="skeletonIndex in 5" :key="skeletonIndex" class="h-14" />
  </div>

  <UiCard v-else-if="currencyStore.rates.length" class="overflow-hidden">
    <UiTable
      :columns="ratesColumns"
      :rows="currencyStore.rates"
      rowClass="hover:bg-accent/40 transition-colors"
    >
      <template #cell-bank_slug="{ row }">
        {{ bankMap[row.bank_slug]?.name || row.bank_slug }}
      </template>
      <template #cell-currency="{ row }">
        <UiBadge>{{ row.currency }}</UiBadge>
      </template>
      <template #cell-buy="{ row }">{{ row.buy?.toFixed(2) }}</template>
      <template #cell-sell="{ row }">{{ row.sell?.toFixed(2) }}</template>
    </UiTable>
  </UiCard>

  <UiEmpty v-else title="No rates found" description="Try adjusting the filters" />
</template>
