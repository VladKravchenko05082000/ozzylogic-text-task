<script setup lang="ts">
import { ref, onMounted } from "vue";
import PagesHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";
import { useCurrencyStore } from "@/stores/currencyStore";

const currencyStore = useCurrencyStore();

const historyColumns: TableColumn[] = [
  { key: "updated_at", label: "Date", tdClass: "text-xs text-muted-foreground" },
  { key: "bank_slug", label: "Bank" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];

const selectedCurrency = ref("USD");
const dateFrom = ref("");
const dateTo = ref("");
const loading = ref(false);
const history = ref<Awaited<ReturnType<typeof currencyStore.fetchHistory>>>([]);

function getToday() {
  return new Date().toISOString().slice(0, 10);
}

function getDaysAgo(days: number) {
  const date = new Date();
  date.setDate(date.getDate() - days);
  return date.toISOString().slice(0, 10);
}

async function load() {
  loading.value = true;
  try {
    history.value = await currencyStore.fetchHistory({
      currencies: [selectedCurrency.value],
      from: dateFrom.value,
      to: dateTo.value,
    });
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  dateFrom.value = getDaysAgo(7);
  dateTo.value = getToday();
  await currencyStore.fetchCurrencies();
});
</script>

<template>
  <PagesHeader title="Exchange rate history" description="Select a currency and date range" />

  <UiCard class="p-4 sm:p-5 mb-6">
    <div class="flex flex-wrap items-end gap-3 max-[428px]:flex-col max-[428px]:items-stretch">
      <div class="min-w-32 max-[428px]:min-w-0">
        <label class="text-xs font-medium text-muted-foreground">Currency</label>
        <select
          v-model="selectedCurrency"
          class="mt-1 flex h-9 w-44 max-[428px]:w-full rounded-md border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option
            v-for="currencyOption in currencyStore.currencies"
            :key="currencyOption"
            :value="currencyOption"
          >
            {{ currencyOption }}
          </option>
        </select>
      </div>
      <div class="flex items-end gap-3 w-fit max-[350px]:flex-col">
        <UiInput v-model="dateFrom" type="date" label="From" class="w-fit" />
        <UiInput v-model="dateTo" type="date" label="To" class="w-fit" />
      </div>
    </div>
    <div class="mt-4">
      <UiButton @click="load" :loading="loading">Show</UiButton>
    </div>
  </UiCard>

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
