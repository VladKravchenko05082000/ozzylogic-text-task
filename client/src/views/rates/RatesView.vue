<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

import { useBanksStore } from "@/stores/banksStore";
import { useCurrencyStore } from "@/stores/currencyStore";
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

const banksStore = useBanksStore();
const currencyStore = useCurrencyStore();

const selectedBanks = ref<string[]>([]);
const selectedCurrencies = ref<string[]>([]);

const bankMap = computed(() =>
  Object.fromEntries(banksStore.banks.map((bank) => [bank.slug, bank]))
);

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
  refresh();
}

function refresh() {
  currencyStore.fetchRates({
    banks: selectedBanks.value,
    currencies: selectedCurrencies.value,
  });
}

onMounted(async () => {
  await Promise.all([
    banksStore.fetchBanks(),
    currencyStore.fetchCurrencies(),
    currencyStore.fetchRates({ banks: [], currencies: [] }),
  ]);
});
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
            v-for="currency in currencyStore.currencies"
            :key="currency"
            @click="toggle(selectedCurrencies, currency)"
            :class="[
              'rounded-md px-3 py-1 text-xs font-medium transition-colors cursor-pointer',
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
            v-for="bank in banksStore.banks"
            :key="bank.slug"
            @click="toggle(selectedBanks, bank.slug)"
            :class="[
              'rounded-md px-3 py-1 text-xs font-medium transition-colors cursor-pointer',
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
  <div v-if="currencyStore.isLoading" class="space-y-2">
    <UiSkeleton v-for="skeletonIndex in 5" :key="skeletonIndex" class="h-14" />
  </div>

  <!-- LIST -->
  <UiCard v-else-if="currencyStore.rates.length" class="overflow-hidden">
    <UiTable :columns="ratesColumns" :rows="currencyStore.rates" rowClass="hover:bg-accent/40 transition-colors">
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
