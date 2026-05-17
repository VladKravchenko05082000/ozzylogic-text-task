import client from "./client";

type RatesFilterParamsType = {
  currencies: string;
  banks: string;
};

type HistoryFilterParamsType = {
  currencies: string;
  from: string;
  to: string;
};

export const currencyApi = {
  listCurrencies: () => client.get("/currency/currency-list"),
  getRates: (params: RatesFilterParamsType) =>
    client.get("currency/latest-currency_list", { params }),
  getSummaryNbuRates: () => client.get("/currency/summary-nbu_rates"),
  getRatesHistory: (params: HistoryFilterParamsType) =>
    client.get("/currency/rates/history", { params }),
};
