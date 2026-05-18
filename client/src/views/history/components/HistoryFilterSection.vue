<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

import { useCurrencyStore, type HistoryRateItem } from "@/stores/currencyStore";

import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UISelect from "@/components/ui/UISelect.vue";

import { getDaysAgo, getToday } from "@/lib/helpers";

const currencyStore = useCurrencyStore();

const emit = defineEmits<{
  result: [history: HistoryRateItem[]];
}>();

const currencyOptions = computed(() =>
  currencyStore.currencies.map((currency) => ({ label: currency, value: currency })),
);

const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    const history = await currencyStore.fetchHistory({
      currencies: [currencyStore.historySelectedCurrency],
      from: currencyStore.historyDateFrom,
      to: currencyStore.historyDateTo,
    });
    emit("result", history);
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  if (!currencyStore.historyDateFrom) currencyStore.historyDateFrom = getDaysAgo(7);
  if (!currencyStore.historyDateTo) currencyStore.historyDateTo = getToday();
  await currencyStore.fetchCurrencies();
});
</script>

<template>
  <div class="flex flex-wrap items-end gap-3 max-[428px]:flex-col max-[428px]:items-stretch">
    <div class="min-w-32 max-[428px]:min-w-0">
      <UISelect
        label="Currency"
        :model-value="currencyStore.historySelectedCurrency"
        :options="currencyOptions"
        class="w-44 max-[428px]:w-full"
        @update:model-value="currencyStore.historySelectedCurrency = $event"
      />
    </div>
    <div class="flex items-end gap-3 w-fit max-[350px]:flex-col">
      <UiInput v-model="currencyStore.historyDateFrom" type="date" label="From" class="w-fit" />
      <UiInput v-model="currencyStore.historyDateTo" type="date" label="To" class="w-fit" />
    </div>
  </div>
  <div class="mt-4">
    <UiButton @click="load" :loading="loading">Show</UiButton>
  </div>
</template>
