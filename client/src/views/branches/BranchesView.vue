<script setup lang="ts">
import { computed, ref } from "vue";
import { useForm } from "@vuehookform/core";
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UiEmpty from "@/components/ui/UiEmpty.vue";
import { nearestBranchesSchema } from "@/schemas/branchesSchema";
import { useBanksStore, type NearestBranch } from "@/stores/banksStore";

const banksStore = useBanksStore();

const { register, handleSubmit, formState, setValue, watch } = useForm({
  schema: nearestBranchesSchema,
  mode: "onTouched",
  defaultValues: {
    maxCount: 10,
    maxDistance: 10,
  },
});

const latValue = watch("lat");
const lngValue = watch("lng");
const maxCountValue = watch("maxCount");
const maxDistanceValue = watch("maxDistance");

const branches = ref<NearestBranch[]>([]);
const geoError = ref<string | null>(null);

const isSubmitDisabled = computed(
  () =>
    formState.value.isSubmitting ||
    banksStore.isLoading ||
    latValue.value == null ||
    lngValue.value == null ||
    !formState.value.isValid,
);

function useGeolocation() {
  geoError.value = null;
  if (!navigator.geolocation) {
    geoError.value = "Geolocation is not supported by your browser";
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      setValue("lat", pos.coords.latitude, { shouldValidate: true });
      setValue("lng", pos.coords.longitude, { shouldValidate: true });
    },
    () => {
      geoError.value = "Failed to retrieve your location";
    },
  );
}

const onSubmit = handleSubmit(async (data) => {
  branches.value = await banksStore.fetchNearestBranches({
    latitude: String(data.lat),
    longitude: String(data.lng),
    distance_limit: String(data.maxDistance),
    limit: data.maxCount,
  });
});
</script>

<template>
  <PageHeader title="Nearest branches" description="Select or enter coordinates" />

  <form @submit="onSubmit">
    <UiCard class="p-4 sm:p-5 mb-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <UiInput
          v-bind="register('lat')"
          type="number"
          step="any"
          label="Latitude (lat)"
          placeholder="50.4501"
          :error="formState.errors.lat ? String(formState.errors.lat) : undefined"
        />
        <UiInput
          v-bind="register('lng')"
          type="number"
          step="any"
          label="Longitude (lng)"
          placeholder="30.5234"
          :error="formState.errors.lng ? String(formState.errors.lng) : undefined"
        />
        <div>
          <label class="text-xs font-medium text-muted-foreground">Count</label>
          <select
            :value="maxCountValue"
            @change="
              setValue('maxCount', Number(($event.target as HTMLSelectElement).value), {
                shouldValidate: true,
              })
            "
            class="mt-1 flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
          </select>
          <p v-if="formState.errors.maxCount" class="mt-1 text-xs text-destructive">
            {{ String(formState.errors.maxCount) }}
          </p>
        </div>
        <div>
          <label class="text-xs font-medium text-muted-foreground">Max distance (km)</label>
          <select
            :value="maxDistanceValue"
            @change="
              setValue('maxDistance', Number(($event.target as HTMLSelectElement).value), {
                shouldValidate: true,
              })
            "
            class="mt-1 flex h-9 w-full rounded-md border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option :value="1">1 km</option>
            <option :value="5">5 km</option>
            <option :value="10">10 km</option>
            <option :value="20">20 km</option>
            <option :value="50">50 km</option>
            <option :value="100">100 km</option>
          </select>
          <p v-if="formState.errors.maxDistance" class="mt-1 text-xs text-destructive">
            {{ String(formState.errors.maxDistance) }}
          </p>
        </div>
      </div>
      <div class="mt-4 flex flex-wrap gap-2">
        <UiButton type="submit" :disabled="isSubmitDisabled" :loading="banksStore.isLoading">
          Search
        </UiButton>
        <UiButton variant="secondary" type="button" @click="useGeolocation">
          Use my location
        </UiButton>
      </div>
      <p v-if="geoError" class="mt-3 text-xs text-destructive">{{ geoError }}</p>
    </UiCard>
  </form>

  <div v-if="branches.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
    <UiCard v-for="(branch, index) in branches" :key="index" class="p-4">
      <div class="flex items-start justify-between gap-2">
        <div class="flex-1 min-w-0">
          <div class="text-sm font-medium truncate">{{ branch.bank_name }}</div>
          <div class="text-xs text-muted-foreground mt-0.5">{{ branch.name || "Branch" }}</div>
        </div>
        <span class="text-xs font-medium text-foreground tabular-nums">
          {{ branch.distance_km }} km
        </span>
      </div>
      <div class="text-xs text-muted-foreground mt-2">{{ branch.address }}</div>
      <div v-if="branch.phone" class="text-xs text-muted-foreground mt-1">{{ branch.phone }}</div>
    </UiCard>
  </div>

  <UiEmpty v-else title="Enter coordinates or click «Use my location»" />
</template>
