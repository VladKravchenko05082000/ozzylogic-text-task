<script setup lang="ts">
type RatesItemType = { bank_slug: string; currency: string; buy: number; sell: number };
type BanksItemType = { slug: string; name: string };

import { ref } from "vue";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

const selectedBanks = ref<string[]>([]);
const selectedCurrencies = ref<string[]>([]);

const currencies = ["USD", "EUR", "GBP", "PLN"];

const banks: BanksItemType[] = [
  { slug: "privatbank", name: "PrivatBank" },
  { slug: "monobank", name: "Monobank" },
  { slug: "oschadbank", name: "Oschadbank" },
  { slug: "ukrsibbank", name: "UkrSibbank" },
];

const bankMap = Object.fromEntries(banks.map((bank) => [bank.slug, bank]));

const rates: RatesItemType[] = [
  { bank_slug: "privatbank", currency: "USD", buy: 39.5, sell: 40.1 },
  { bank_slug: "privatbank", currency: "EUR", buy: 43.2, sell: 44.0 },
  { bank_slug: "monobank", currency: "USD", buy: 39.8, sell: 40.3 },
  { bank_slug: "monobank", currency: "EUR", buy: 43.5, sell: 44.2 },
  { bank_slug: "monobank", currency: "GBP", buy: 50.1, sell: 51.0 },
  { bank_slug: "oschadbank", currency: "USD", buy: 39.3, sell: 40.0 },
  { bank_slug: "oschadbank", currency: "PLN", buy: 9.6, sell: 9.9 },
  { bank_slug: "ukrsibbank", currency: "USD", buy: 39.6, sell: 40.2 },
  { bank_slug: "ukrsibbank", currency: "EUR", buy: 43.1, sell: 43.9 },
];

const isLoading = false;

const ratesColumns: TableColumn[] = [
  { key: "bank_slug", label: "Bank", tdClass: "font-medium" },
  { key: "currency", label: "Currency" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];

function toggle(list: string[], value: string) {
  const index = list.indexOf(value);
  if (index === -1) list.push(value);
  else list.splice(index, 1);
}
</script>

<template>
  <PageHeader title="Exchange Rates" description="Current buy and sell rates across all banks" />

  <!-- FILTERS -->
  <UiCard class="mb-6 p-4 sm:p-5">
    <div class="space-y-4">
      <div>
        <div class="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Currencies
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="currency in currencies"
            :key="currency"
            @click="toggle(selectedCurrencies, currency)"
            :class="[
              'rounded-md px-3 py-1 text-xs font-medium transition-colors',
              selectedCurrencies.includes(currency)
                ? 'bg-primary text-primary-foreground'
                : 'bg-secondary text-secondary-foreground hover:bg-secondary/70',
            ]"
          >
            {{ currency }}
          </button>
        </div>
      </div>

      <div>
        <div class="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Banks
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="bank in banks"
            :key="bank.slug"
            @click="toggle(selectedBanks, bank.slug)"
            :class="[
              'rounded-md px-3 py-1 text-xs font-medium transition-colors',
              selectedBanks.includes(bank.slug)
                ? 'bg-primary text-primary-foreground'
                : 'bg-secondary text-secondary-foreground hover:bg-secondary/70',
            ]"
          >
            {{ bank.name }}
          </button>
        </div>
      </div>
    </div>
  </UiCard>

  <!-- LOADING -->
  <div v-if="isLoading" class="space-y-2">
    <UiSkeleton v-for="skeletonIndex in 5" :key="skeletonIndex" class="h-14" />
  </div>

  <!-- LIST -->
  <UiCard v-else-if="rates.length" class="overflow-hidden">
    <UiTable :columns="ratesColumns" :rows="rates" rowClass="hover:bg-accent/40 transition-colors">
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
