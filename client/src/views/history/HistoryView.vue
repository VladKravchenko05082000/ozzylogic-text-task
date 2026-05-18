<script setup lang="ts">
import { ref, onMounted } from "vue";

import PagesHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";
import HistoryFilterSection from "./components/HistoryFilterSection.vue";
import { useCurrencyStore, type HistoryRateItem } from "@/stores/currencyStore";

const currencyStore = useCurrencyStore();

const history = ref<HistoryRateItem[]>([]);

function handleResult(data: HistoryRateItem[]) {
  history.value = data;
}

onMounted(() => {
  history.value = currencyStore.history;
});

const historyColumns: TableColumn[] = [
  { key: "updated_at", label: "Date", tdClass: "text-xs text-muted-foreground" },
  { key: "bank_slug", label: "Bank" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];
</script>

<template>
  <PagesHeader title="Exchange rate history" description="Select a currency and date range" />

  <UiCard class="p-4 sm:p-5 mb-6"><HistoryFilterSection @result="handleResult" /></UiCard>

  <UiCard v-if="history.length" class="overflow-hidden">
    <div class="p-4 border-b border-border">
      <h3 class="text-sm font-medium">Rate records</h3>
      <p class="text-xs text-muted-foreground mt-0.5">
        {{ history.length }} entries for the period
      </p>
    </div>
    <UiTable :columns="historyColumns" :rows="history" compact>
      <template #cell-buy="{ row }">{{ row.buy?.toFixed(2) }}</template>
      <template #cell-sell="{ row }">{{ row.sell?.toFixed(2) }}</template>
    </UiTable>
  </UiCard>

  <UiEmpty v-else title="Select filters and click «Show»" />
</template>
