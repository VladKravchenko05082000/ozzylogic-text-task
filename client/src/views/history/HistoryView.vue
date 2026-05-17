<script setup lang="ts">
import { ref, computed } from "vue";
import PagesHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

interface HistoryEntry {
  recorded_at: string;
  bank_slug: string;
  currency: string;
  buy: number | null;
  sell: number | null;
}

interface BankOption {
  slug: string;
  name: string;
}

const currencies: string[] = ["USD", "EUR", "GBP", "PLN", "CHF"];

const bankOptions: BankOption[] = [
  { slug: "privatbank", name: "PrivatBank" },
  { slug: "monobank", name: "Monobank" },
  { slug: "oschadbank", name: "Oschadbank" },
  { slug: "ukrsibbank", name: "UkrSibbank" },
  { slug: "raiffeisen", name: "Raiffeisen Bank" },
];

const mockHistory: HistoryEntry[] = [
  { recorded_at: "2026-05-10", bank_slug: "privatbank", currency: "USD", buy: 39.3, sell: 39.9 },
  { recorded_at: "2026-05-10", bank_slug: "monobank", currency: "USD", buy: 39.5, sell: 40.1 },
  { recorded_at: "2026-05-11", bank_slug: "privatbank", currency: "USD", buy: 39.45, sell: 40.05 },
  { recorded_at: "2026-05-11", bank_slug: "oschadbank", currency: "USD", buy: 38.9, sell: 39.7 },
  { recorded_at: "2026-05-12", bank_slug: "monobank", currency: "USD", buy: 39.6, sell: 40.2 },
  { recorded_at: "2026-05-12", bank_slug: "raiffeisen", currency: "USD", buy: 39.2, sell: 40.0 },
  { recorded_at: "2026-05-13", bank_slug: "privatbank", currency: "EUR", buy: 42.5, sell: 43.3 },
  { recorded_at: "2026-05-13", bank_slug: "monobank", currency: "EUR", buy: 42.8, sell: 43.6 },
  { recorded_at: "2026-05-14", bank_slug: "ukrsibbank", currency: "EUR", buy: 42.1, sell: 43.0 },
  { recorded_at: "2026-05-14", bank_slug: "oschadbank", currency: "EUR", buy: 42.0, sell: 42.9 },
  { recorded_at: "2026-05-15", bank_slug: "privatbank", currency: "GBP", buy: 49.0, sell: 50.2 },
  { recorded_at: "2026-05-15", bank_slug: "raiffeisen", currency: "GBP", buy: 49.2, sell: 50.4 },
  { recorded_at: "2026-05-16", bank_slug: "monobank", currency: "PLN", buy: 9.5, sell: 10.0 },
  { recorded_at: "2026-05-16", bank_slug: "privatbank", currency: "PLN", buy: 9.6, sell: 10.1 },
  { recorded_at: "2026-05-17", bank_slug: "ukrsibbank", currency: "CHF", buy: 44.0, sell: 45.2 },
  { recorded_at: "2026-05-17", bank_slug: "oschadbank", currency: "CHF", buy: 43.8, sell: 45.0 },
];

const historyColumns: TableColumn[] = [
  { key: "recorded_at", label: "Date", tdClass: "text-xs text-muted-foreground" },
  { key: "bank_slug", label: "Bank" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];

const currency = ref("USD");
const bank = ref("");
const dateFrom = ref("2026-05-10");
const dateTo = ref("2026-05-17");
const loading = ref(false);
const searched = ref(false);

const history = ref<HistoryEntry[]>([]);

const filtered = computed(() =>
  mockHistory.filter((h) => {
    if (h.currency !== currency.value) return false;
    if (bank.value && h.bank_slug !== bank.value) return false;
    if (dateFrom.value && h.recorded_at < dateFrom.value) return false;
    if (dateTo.value && h.recorded_at > dateTo.value) return false;
    return true;
  }),
);

function load() {
  loading.value = true;
  setTimeout(() => {
    history.value = filtered.value;
    searched.value = true;
    loading.value = false;
  }, 400);
}
</script>

<template>
  <PagesHeader title="Exchange rate history" description="Select a currency and date range" />

  <UiCard class="p-4 sm:p-5 mb-6">
    <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
      <div>
        <label class="text-xs font-medium text-muted-foreground">Currency</label>
        <select
          v-model="currency"
          class="mt-1 flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option v-for="c in currencies" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div>
        <label class="text-xs font-medium text-muted-foreground">Bank</label>
        <select
          v-model="bank"
          class="mt-1 flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">All</option>
          <option v-for="b in bankOptions" :key="b.slug" :value="b.slug">{{ b.name }}</option>
        </select>
      </div>
      <UiInput v-model="dateFrom" type="date" label="From" />
      <UiInput v-model="dateTo" type="date" label="To" />
    </div>
    <div class="mt-4">
      <UiButton @click="load" :loading="loading">Show</UiButton>
    </div>
  </UiCard>

  <div class="p-4 border-b border-border">
    <h3 class="text-sm font-medium">Rate records</h3>
    <p class="text-xs text-muted-foreground mt-0.5">{{ history.length }} entries for the period</p>
  </div>
  <UiCard v-if="history.length" class="overflow-hidden">
    <UiTable :columns="historyColumns" :rows="history" compact>
      <template #cell-buy="{ row }">{{ row.buy?.toFixed(2) }}</template>
      <template #cell-sell="{ row }">{{ row.sell?.toFixed(2) }}</template>
    </UiTable>
  </UiCard>

  <UiEmpty v-else title="Select filters and click «Show»" />
</template>
