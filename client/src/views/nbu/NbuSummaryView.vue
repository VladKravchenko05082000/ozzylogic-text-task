<script setup lang="ts">
import { computed, onMounted } from "vue";

import { useCurrencyStore } from "@/stores/currencyStore";
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

interface RateRow {
  currency: string;
  nbu: number | null;
  buy: number | null;
  sell: number | null;
}

const currencyStore = useCurrencyStore();

const columns: TableColumn[] = [
  { key: "currency", label: "Currency" },
  { key: "nbu", label: "NBU", align: "right" },
  { key: "buy", label: "Avg. buy", align: "right" },
  { key: "sell", label: "Avg. sell", align: "right" },
];

const rows = computed<RateRow[]>(() => {
  const map: Record<string, RateRow> = {};

  for (const nbuRate of currencyStore.summaryNbuRatesList.nbu_latest_rates) {
    map[nbuRate.currency] = { currency: nbuRate.currency, nbu: nbuRate.rate, buy: null, sell: null };
  }

  for (const bankRate of currencyStore.summaryNbuRatesList.average_banks_rates) {
    if (!map[bankRate.currency]) {
      map[bankRate.currency] = { currency: bankRate.currency, nbu: null, buy: null, sell: null };
    }
    const row = map[bankRate.currency]!;
    row.buy = bankRate.avg_buy;
    row.sell = bankRate.avg_sell;
  }

  return Object.values(map);
});

onMounted(() => currencyStore.fetchNbuSummaryRates());
</script>

<template>
  <PageHeader
    title="NBU & average bank rates"
    description="Comparison of the official NBU rate with the average across 5 banks"
  />

  <div v-if="currencyStore.isLoading" class="space-y-2">
    <UiSkeleton v-for="i in 5" :key="i" class="h-12" />
  </div>

  <UiCard v-else class="overflow-hidden">
    <UiTable :columns="columns" :rows="rows">
      <template #cell-currency="{ row }">
        <UiBadge>{{ row.currency }}</UiBadge>
      </template>
      <template #cell-nbu="{ row }">{{ row.nbu?.toFixed(4) ?? "—" }}</template>
      <template #cell-buy="{ row }">{{ row.buy?.toFixed(4) ?? "—" }}</template>
      <template #cell-sell="{ row }">{{ row.sell?.toFixed(4) ?? "—" }}</template>
    </UiTable>
  </UiCard>
</template>
