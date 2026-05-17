import { ref, onMounted, onUnmounted } from "vue";

export function useBreakpoint(breakpoint: number = 768) {
  const isDesktop = ref<boolean>(false);

  function update() {
    isDesktop.value = window.innerWidth >= breakpoint;
  }

  onMounted(() => {
    update();
    window.addEventListener("resize", update);
  });

  onUnmounted(() => {
    window.removeEventListener("resize", update);
  });

  return { isDesktop };
}
