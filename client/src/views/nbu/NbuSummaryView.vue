<script setup lang="ts">
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

interface RateRow {
  currency: string;
  nbu: number | null;
  avg_buy: number | null;
  avg_sell: number | null;
}

const columns: TableColumn[] = [
  { key: "currency", label: "Currency" },
  { key: "nbu", label: "NBU", align: "right" },
  { key: "avg_buy", label: "Avg. buy", align: "right" },
  { key: "avg_sell", label: "Avg. sell", align: "right" },
];

const rows: RateRow[] = [
  { currency: "USD", nbu: 41.2311, avg_buy: 39.5, avg_sell: 40.1 },
  { currency: "EUR", nbu: 44.987, avg_buy: 42.8, avg_sell: 43.6 },
  { currency: "GBP", nbu: 52.1045, avg_buy: 49.2, avg_sell: 50.4 },
  { currency: "PLN", nbu: 10.312, avg_buy: 9.6, avg_sell: 10.1 },
  { currency: "CHF", nbu: 46.754, avg_buy: 44.1, avg_sell: 45.3 },
  { currency: "JPY", nbu: 0.2734, avg_buy: null, avg_sell: null },
];
</script>

<template>
  <PageHeader
    title="NBU & average bank rates"
    description="Comparison of the official NBU rate with the average across 5 banks"
  />

  <UiCard class="overflow-hidden">
    <UiTable :columns="columns" :rows="rows">
      <template #cell-currency="{ row }">
        <UiBadge>{{ row.currency }}</UiBadge>
      </template>
      <template #cell-nbu="{ row }">{{ row.nbu?.toFixed(4) ?? "—" }}</template>
      <template #cell-avg_buy="{ row }">{{ row.avg_buy?.toFixed(4) ?? "—" }}</template>
      <template #cell-avg_sell="{ row }">{{ row.avg_sell?.toFixed(4) ?? "—" }}</template>
    </UiTable>
  </UiCard>
</template>
