import { banksApi } from "@/api/banks";
import { defineStore } from "pinia";
import { ref } from "vue";

type BanksViewListItemType = {
  slug: string;
  name: string;
  phone: string;
  rating: number;
  logo: string | null;
};

type Rate = {
  currency: string;
  buy: number;
  sell: number;
};

type Branch = {
  name: string;
  address: string;
  phone?: string;
};

type BankDetailType = {
  name: string;
  description: string;
  site: string;
  phone: string | null;
  email: string | null;
  rating: number | null;
  legal_address: string | null;
};

type BankInfoType = {
  bank: BankDetailType;
  rates: Rate[];
  branches: Branch[];
};

type BanksListResponse = {
  banks: BanksViewListItemType[];
};

export type NearestBranch = {
  bank_name: string;
  name: string;
  address: string;
  phone: string | null;
  distance_km: number;
};

type NearestBranchesResponse = {
  branches: NearestBranch[];
};

type NearestBranchParamsType = {
  latitude: string;
  longitude: string;
  distance_limit?: string;
  limit?: number;
};

export const useBanksStore = defineStore("banks", () => {
  const banks = ref<BanksViewListItemType[]>([]);
  const currentBank = ref<BankInfoType | null>(null);
  const summary = ref({ nbu: [], banks_average: [] });
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchBanks(): Promise<BanksViewListItemType[]> {
    isLoading.value = true;
    error.value = null;
    try {
      const { data }: { data: BanksListResponse } = await banksApi.listBanks();
      banks.value = data.banks;
      return data.banks;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchBank(slug: string): Promise<BankInfoType | null> {
    isLoading.value = true;
    error.value = null;
    try {
      const { data }: { data: BankInfoType } = await banksApi.getBank(slug);
      currentBank.value = data;
      return data;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchNearestBranches(filters: NearestBranchParamsType): Promise<NearestBranch[]> {
    isLoading.value = true;
    error.value = null;
    try {
      const params: NearestBranchParamsType = {
        latitude: filters.latitude,
        longitude: filters.longitude,
        distance_limit: filters.distance_limit ?? "",
        limit: filters.limit,
      };
      const { data }: { data: NearestBranchesResponse } = await banksApi.getNearestBranches(params);
      return data.branches;
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : String(e);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  return {
    banks,
    currentBank,
    summary,
    isLoading,
    error,
    fetchBanks,
    fetchBank,
    fetchNearestBranches,
  };
});
