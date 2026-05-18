<script setup lang="ts">
import { ref, onMounted } from "vue";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import BranchesFilterForm from "./components/BranchesFilterForm.vue";
import BranchesCard from "./components/BranchesCard.vue";

import { useBanksStore, type NearestBranch } from "@/stores/banksStore";

const banksStore = useBanksStore();
const branches = ref<NearestBranch[]>([]);

function handleResult(data: NearestBranch[]) {
  branches.value = data;
}

onMounted(() => {
  branches.value = banksStore.nearestBranches;
});
</script>

<template>
  <PageHeader title="Nearest branches" description="Select or enter coordinates" />

  <BranchesFilterForm @result="handleResult" />

  <div v-if="branches.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
    <UiCard v-for="(branch, index) in branches" :key="index" class="p-4">
      <BranchesCard
        :bank_name="branch.bank_name"
        :name="branch.name"
        :address="branch.address"
        :phone="branch.phone"
        :distance_km="branch.distance_km"
      />
    </UiCard>
  </div>

  <UiEmpty v-else title="Enter coordinates or click «Use my location»" />
</template>
