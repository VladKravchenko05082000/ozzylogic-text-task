<script setup lang="ts">
type BanksViewListType = {
  slug: string;
  name: string;
  phone: string;
  rating: number;
  logo_url: string | null;
};

import { RouterLink } from "vue-router";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";

const banks: BanksViewListType[] = [
  {
    slug: "privatbank",
    name: "PrivatBank",
    phone: "+380 (44) 708-88-88",
    rating: 4.5,
    logo_url:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Privatbank_logo_eng.svg/320px-Privatbank_logo_eng.svg.png",
  },
  {
    slug: "monobank",
    name: "Monobank",
    phone: "+380 (44) 000-00-00",
    rating: 4.8,
    logo_url:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Monobank_logo_2019.svg/320px-Monobank_logo_2019.svg.png",
  },
  {
    slug: "oschadbank",
    name: "Oschadbank",
    phone: "+380 (800) 210-800",
    rating: 3.9,
    logo_url:
      "https://upload.wikimedia.org/wikipedia/uk/thumb/3/3d/Oschadbank_logo_uk.svg/320px-Oschadbank_logo_uk.svg.png",
  },
  {
    slug: "ukrsibbank",
    name: "UkrSibbank",
    phone: "+380 (44) 230-33-33",
    rating: 4.1,
    logo_url: null,
  },
  {
    slug: "raiffeisen",
    name: "Raiffeisen Bank",
    phone: "+380 (44) 495-88-88",
    rating: 4.3,
    logo_url: null,
  },
];
</script>

<template>
  <PageHeader title="Banks" description="5 banks supported by the service" />

  <div v-if="banks.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
    <RouterLink v-for="bank in banks" :key="bank.slug" :to="`/banks/${bank.slug}`" class="block">
      <UiCard hoverable class="p-4 h-full">
        <div class="flex items-start gap-3">
          <div
            v-if="bank.logo_url"
            class="h-10 w-10 shrink-0 rounded-md bg-muted overflow-hidden flex items-center justify-center"
          >
            <img :src="bank.logo_url" :alt="bank.name" class="h-full w-full object-contain" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-medium truncate">{{ bank.name }}</h3>
            <p class="text-xs text-muted-foreground mt-0.5">
              {{ bank.phone || "—" }}
            </p>
            <p v-if="bank.rating" class="text-xs text-muted-foreground mt-1">
              Rating: {{ bank.rating }}
            </p>
          </div>
        </div>
      </UiCard>
    </RouterLink>
  </div>

  <UiEmpty v-else title="No banks found" />
</template>
