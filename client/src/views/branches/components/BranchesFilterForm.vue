<script setup lang="ts">
import { computed } from "vue";
import { useForm } from "@vuehookform/core";
import UiCard from "@/components/ui/UiCard.vue";
import UiButton from "@/components/ui/UiButton.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UISelect from "@/components/ui/UISelect.vue";
import { nearestBranchesSchema } from "@/schemas/branchesSchema";
import { useBanksStore, type NearestBranch } from "@/stores/banksStore";
import { useGeolocation } from "@/composables/useGeolocation";

const emit = defineEmits<{
  result: [branches: NearestBranch[]];
}>();

const banksStore = useBanksStore();

const { register, handleSubmit, formState, setValue, watch } = useForm({
  schema: nearestBranchesSchema,
  mode: "onTouched",
  defaultValues: {
    lat: banksStore.branchesLat ?? undefined,
    lng: banksStore.branchesLng ?? undefined,
    maxCount: banksStore.branchesMaxCount,
    maxDistance: banksStore.branchesMaxDistance,
  },
});

const latValue = watch("lat");
const lngValue = watch("lng");
const maxCountValue = watch("maxCount");
const maxDistanceValue = watch("maxDistance");

const { geoError, getLocation } = useGeolocation((lat, lng) => {
  setValue("lat", lat, { shouldValidate: true });
  setValue("lng", lng, { shouldValidate: true });
});

const isSubmitDisabled = computed(
  () =>
    formState.value.isSubmitting ||
    banksStore.isLoading ||
    latValue.value == null ||
    lngValue.value == null ||
    !formState.value.isValid,
);

const countOptions = [
  { label: "5", value: "5" },
  { label: "10", value: "10" },
  { label: "20", value: "20" },
  { label: "50", value: "50" },
];

const distanceOptions = [
  { label: "1 km", value: "1" },
  { label: "5 km", value: "5" },
  { label: "10 km", value: "10" },
  { label: "20 km", value: "20" },
  { label: "50 km", value: "50" },
  { label: "100 km", value: "100" },
];

const onSubmit = handleSubmit(async (data) => {
  banksStore.branchesLat = data.lat;
  banksStore.branchesLng = data.lng;
  banksStore.branchesMaxCount = data.maxCount;
  banksStore.branchesMaxDistance = data.maxDistance;
  const branches = await banksStore.fetchNearestBranches({
    latitude: String(data.lat),
    longitude: String(data.lng),
    distance_limit: String(data.maxDistance),
    limit: data.maxCount,
  });
  emit("result", branches);
});
</script>

<template>
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
        <UISelect
          label="Count"
          :model-value="String(maxCountValue)"
          :options="countOptions"
          :error="formState.errors.maxCount ? String(formState.errors.maxCount) : undefined"
          @update:model-value="setValue('maxCount', Number($event), { shouldValidate: true })"
        />
        <UISelect
          label="Max distance (km)"
          :model-value="String(maxDistanceValue)"
          :options="distanceOptions"
          :error="formState.errors.maxDistance ? String(formState.errors.maxDistance) : undefined"
          @update:model-value="setValue('maxDistance', Number($event), { shouldValidate: true })"
        />
      </div>
      <div class="mt-4 flex flex-wrap gap-2">
        <UiButton type="submit" :disabled="isSubmitDisabled" :loading="banksStore.isLoading">
          Search
        </UiButton>
        <UiButton variant="secondary" type="button" @click="getLocation">
          Use my location
        </UiButton>
      </div>
      <p v-if="geoError" class="mt-3 text-xs text-destructive">{{ geoError }}</p>
    </UiCard>
  </form>
</template>
