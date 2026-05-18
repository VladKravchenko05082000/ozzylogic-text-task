<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";

import { useBanksStore } from "@/stores/banksStore";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import BankDetailInfo from "./components/BankDetailsInfo.vue";
import BankDetailsBranches from "./components/BankDetailsBranches.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiSkeleton from "@/components/ui/UiSkeleton.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

const rateColumns: TableColumn[] = [
  { key: "currency", label: "Currency" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];
const route = useRoute();
const bankStore = useBanksStore();

onMounted(() => bankStore.fetchBank(route.params.slug as string));
</script>

<template>
  <div>
    <div v-if="bankStore.isLoading" class="space-y-4">
      <UiSkeleton class="h-24" />
      <UiSkeleton class="h-40" />
    </div>

    <div v-if="bankStore.currentBank && !bankStore.isLoading">
      <PageHeader
        :title="bankStore.currentBank.bank.name"
        :description="bankStore.currentBank.bank.description"
      />

      <UiCard class="p-5 mb-6">
        <BankDetailInfo
          :site="bankStore.currentBank.bank.site"
          :phone="bankStore.currentBank.bank.phone"
          :email="bankStore.currentBank.bank.email"
          :rating="bankStore.currentBank.bank.rating"
          :legal_address="bankStore.currentBank.bank.legal_address"
        />
      </UiCard>

      <!-- RATES -->
      <h2 class="text-sm font-semibold mb-3">Current rates</h2>
      <UiCard class="overflow-hidden mb-6">
        <UiTable
          v-if="bankStore.currentBank.rates.length"
          :columns="rateColumns"
          :rows="bankStore.currentBank.rates"
        >
          <template #cell-currency="{ row }">
            <UiBadge>{{ row.currency }}</UiBadge>
          </template>
          <template #cell-buy="{ row }">{{ row.buy.toFixed(2) }}</template>
          <template #cell-sell="{ row }">{{ row.sell.toFixed(2) }}</template>
        </UiTable>
        <p v-else class="p-4 text-sm text-muted-foreground">No rates available</p>
      </UiCard>

      <h2 class="text-sm font-semibold mb-3">
        Branches
        <span class="text-xs text-muted-foreground font-normal"
          >({{ bankStore.currentBank.branches.length }})</span
        >
      </h2>

      <div
        v-if="bankStore.currentBank.branches.length"
        class="grid grid-cols-1 md:grid-cols-2 gap-3"
      >
        <UiCard v-for="(branch, i) in bankStore.currentBank.branches" :key="i" class="p-3">
          <BankDetailsBranches
            :name="branch.name"
            :address="branch.address"
            :phone="branch.phone"
          />
        </UiCard>
      </div>
      <p v-else class="text-sm text-muted-foreground">No branches available</p>
    </div>
  </div>
</template>
