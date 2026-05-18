import { ref } from "vue";

export function useGeolocation(onSuccess: (lat: number, lng: number) => void) {
  const geoError = ref<string | null>(null);

  function getLocation() {
    geoError.value = null;
    if (!navigator.geolocation) {
      geoError.value = "Geolocation is not supported by your browser";
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => onSuccess(pos.coords.latitude, pos.coords.longitude),
      () => {
        geoError.value = "Failed to retrieve your location";
      },
    );
  }

  return { geoError, getLocation };
}
