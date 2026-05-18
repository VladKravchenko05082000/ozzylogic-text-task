import { defineStore } from "pinia";
import { ref } from "vue";

import { currencyApi } from "@/api/currency";

type RatesFilterParamsType = {
  currencies: string[];
  banks: string[];
};

type RateItemType = {
  bank_slug: string;
  currency: string;
  buy: number;
  sell: number;
};

type CurrencyListResponse = {
  currency_list: string[];
};

type RatesResponse = {
  total: number;
  latest_rates: RateItemType[];
};

type NbuRatesItem = {
  currency: string;
  rate: number;
};

type BanksAvarageItem = {
  currency: string;
  avg_buy: number;
  avg_sell: number;
};

type NbuSummaryRatesItem = {
  nbu_latest_rates: NbuRatesItem[];
  average_banks_rates: BanksAvarageItem[];
};

type HistoryFilterParamsType = {
  currencies: string[];
  from: string;
  to: string;
};

export type HistoryRateItem = {
  bank_slug: string;
  currency: string;
  buy: number;
  sell: number;
  updated_at: string;
};

type HistoryResponse = {
  history: HistoryRateItem[];
};

export const useCurrencyStore = defineStore("currency", () => {
  const currencies = ref<string[]>([]);
  const rates = ref<RateItemType[]>([]);
  const selectedBanks = ref<string[]>([]);
  const selectedCurrencies = ref<string[]>([]);
  const history = ref<HistoryRateItem[]>([]);
  const historySelectedCurrency = ref("USD");
  const historyDateFrom = ref("");
  const historyDateTo = ref("");
  const summaryNbuRatesList = ref<NbuSummaryRatesItem>({
    nbu_latest_rates: [],
    average_banks_rates: [],
  });

  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchCurrencies(): Promise<string[]> {
    try {
      const { data }: { data: CurrencyListResponse } = await currencyApi.listCurrencies();
      currencies.value = data.currency_list;
      return data.currency_list;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return [];
    }
  }

  async function fetchRates(filters: RatesFilterParamsType): Promise<RateItemType[]> {
    isLoading.value = true;
    error.value = null;
    try {
      const params: Partial<{ banks: string; currencies: string }> = {};
      if (filters.banks?.length) params.banks = filters.banks.join(",");
      if (filters.currencies?.length) params.currencies = filters.currencies.join(",");
      const { data }: { data: RatesResponse } = await currencyApi.getRates(
        params as { currencies: string; banks: string },
      );
      rates.value = data.latest_rates;
      return data.latest_rates;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchNbuSummaryRates(): Promise<NbuSummaryRatesItem | null> {
    isLoading.value = true;
    error.value = null;
    try {
      const { data }: { data: NbuSummaryRatesItem } = await currencyApi.getSummaryNbuRates();
      summaryNbuRatesList.value = data;
      return data;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchHistory(filters: HistoryFilterParamsType): Promise<HistoryRateItem[]> {
    isLoading.value = true;
    error.value = null;
    try {
      const params = {
        currencies: filters.currencies.join(","),
        from: filters.from,
        to: filters.to,
      };
      const { data }: { data: HistoryResponse } = await currencyApi.getRatesHistory(params);
      history.value = data.history;
      return data.history;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  function clearCurrency() {
    currencies.value = [];
    rates.value = [];
    selectedBanks.value = [];
    selectedCurrencies.value = [];
    history.value = [];
    historySelectedCurrency.value = "USD";
    historyDateFrom.value = "";
    historyDateTo.value = "";
  }

  return {
    currencies,
    rates,
    selectedBanks,
    selectedCurrencies,
    history,
    historySelectedCurrency,
    historyDateFrom,
    historyDateTo,
    summaryNbuRatesList,
    isLoading,
    error,
    clearCurrency,
    fetchCurrencies,
    fetchRates,
    fetchNbuSummaryRates,
    fetchHistory,
  };
});
