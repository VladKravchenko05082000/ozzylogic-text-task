<script setup lang="ts">
import { useBanksStore } from "@/stores/banksStore";
import { useCurrencyStore } from "@/stores/currencyStore";

const banksStore = useBanksStore();
const currencyStore = useCurrencyStore();

function toggle(list: string[], value: string) {
  const index = list.indexOf(value);
  if (index === -1) list.push(value);
  else list.splice(index, 1);
  currencyStore.fetchRates({
    banks: currencyStore.selectedBanks,
    currencies: currencyStore.selectedCurrencies,
  });
}
</script>

<template>
  <div class="space-y-4">
    <div>
      <div class="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
        Currencies
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="currency in currencyStore.currencies"
          :key="currency"
          @click="toggle(currencyStore.selectedCurrencies, currency)"
          :class="[
            'rounded-md px-3 py-1 text-xs font-medium transition-colors cursor-pointer',
            currencyStore.selectedCurrencies.includes(currency)
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
          @click="toggle(currencyStore.selectedBanks, bank.slug)"
          :class="[
            'rounded-md px-3 py-1 text-xs font-medium transition-colors cursor-pointer',
            currencyStore.selectedBanks.includes(bank.slug)
              ? 'bg-primary text-primary-foreground'
              : 'bg-secondary text-secondary-foreground hover:bg-secondary/70',
          ]"
        >
          {{ bank.name }}
        </button>
      </div>
    </div>
  </div>
</template>
