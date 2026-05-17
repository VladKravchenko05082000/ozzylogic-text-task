<script setup lang="ts">
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiBadge from "@/components/ui/UiBadge.vue";
import UiTable, { type TableColumn } from "@/components/ui/UiTable.vue";

interface Rate {
  currency: string;
  buy: number;
  sell: number;
}

interface Branch {
  name: string;
  address: string;
  phone?: string;
}

interface Bank {
  name: string;
  description: string;
  site: string;
  phone: string | null;
  email: string | null;
  rating: number | null;
  legal_address: string | null;
  rates: Rate[];
  branches: Branch[];
}

const rateColumns: TableColumn[] = [
  { key: "currency", label: "Currency" },
  { key: "buy", label: "Buy", align: "right" },
  { key: "sell", label: "Sell", align: "right" },
];

const bank: Bank = {
  name: "PrivatBank",
  description: "The largest commercial bank in Ukraine",
  site: "https://privatbank.ua",
  phone: "+380 (44) 708-88-88",
  email: "support@privatbank.ua",
  rating: 4.5,
  legal_address: "1D Naberezhna Peremohy St., Dnipro, 49094, Ukraine",
  rates: [
    { currency: "USD", buy: 39.5, sell: 40.1 },
    { currency: "EUR", buy: 42.8, sell: 43.6 },
    { currency: "GBP", buy: 49.2, sell: 50.4 },
    { currency: "PLN", buy: 9.6, sell: 10.1 },
  ],
  branches: [
    { name: "Branch №1", address: "12 Khreshchatyk St., Kyiv", phone: "+380 (44) 111-11-11" },
    { name: "Branch №2", address: "5 Sumska St., Kharkiv", phone: "+380 (57) 222-22-22" },
    { name: "Branch №3", address: "27 Derybasivska St., Odesa", phone: "+380 (48) 333-33-33" },
    { name: "Branch №4", address: "3 Prospekt Svobody, Lviv", phone: "+380 (32) 444-44-44" },
    { name: "Branch №5", address: "8 Soborna St., Dnipro", phone: "+380 (56) 555-55-55" },
  ],
};
</script>

<template>
  <div>
    <PageHeader :title="bank.name" :description="bank.description" />

    <!-- INFO -->
    <UiCard class="p-5 mb-6">
      <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        <div>
          <dt class="text-xs text-muted-foreground">Website</dt>
          <dd class="mt-0.5">
            <a :href="bank.site" target="_blank" class="text-info hover:underline">
              {{ bank.site }}
            </a>
          </dd>
        </div>
        <div>
          <dt class="text-xs text-muted-foreground">Phone</dt>
          <dd class="mt-0.5">{{ bank.phone || "—" }}</dd>
        </div>
        <div>
          <dt class="text-xs text-muted-foreground">Email</dt>
          <dd class="mt-0.5">{{ bank.email || "—" }}</dd>
        </div>
        <div>
          <dt class="text-xs text-muted-foreground">Rating</dt>
          <dd class="mt-0.5">{{ bank.rating || "—" }}</dd>
        </div>
        <div class="sm:col-span-2">
          <dt class="text-xs text-muted-foreground">Legal address</dt>
          <dd class="mt-0.5">{{ bank.legal_address || "—" }}</dd>
        </div>
      </dl>
    </UiCard>

    <!-- RATES -->
    <h2 class="text-sm font-semibold mb-3">Current rates</h2>
    <UiCard class="overflow-hidden mb-6">
      <UiTable v-if="bank.rates.length" :columns="rateColumns" :rows="bank.rates">
        <template #cell-currency="{ row }">
          <UiBadge>{{ row.currency }}</UiBadge>
        </template>
        <template #cell-buy="{ row }">{{ row.buy.toFixed(2) }}</template>
        <template #cell-sell="{ row }">{{ row.sell.toFixed(2) }}</template>
      </UiTable>
      <p v-else class="p-4 text-sm text-muted-foreground">No rates available</p>
    </UiCard>

    <!-- BRANCHES -->
    <h2 class="text-sm font-semibold mb-3">
      Branches
      <span class="text-xs text-muted-foreground font-normal">({{ bank.branches.length }})</span>
    </h2>
    <div v-if="bank.branches.length" class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <UiCard v-for="(br, i) in bank.branches" :key="i" class="p-3">
        <div class="text-sm font-medium">{{ br.name || "Branch" }}</div>
        <div class="text-xs text-muted-foreground mt-1">{{ br.address }}</div>
        <div v-if="br.phone" class="text-xs text-muted-foreground mt-0.5">{{ br.phone }}</div>
      </UiCard>
    </div>
    <p v-else class="text-sm text-muted-foreground">No branches available</p>
  </div>
</template>
