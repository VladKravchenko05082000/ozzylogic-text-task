<script setup lang="ts">
import { computed, ref } from "vue";
import { useForm } from "@vuehookform/core";

import { useUserStore } from "@/stores/userStore";

import UiInput from "@/components/ui/UiInput.vue";
import UiButton from "@/components/ui/UiButton.vue";

import { profileSchema } from "@/schemas/profileSchema";

const userStore = useUserStore();
const isSuccess = ref(false);

const { register, handleSubmit, formState, watch, setError } = useForm({
  schema: profileSchema,
  defaultValues: {
    email: userStore.user?.email ?? "",
  },
  mode: "onBlur",
});

const emailValue = watch("email");

const isSubmitDisabled = computed(
  () => formState.value.isSubmitting || !emailValue.value || !formState.value.isValid,
);

const onSubmit = handleSubmit(async (data: { email: string }) => {
  isSuccess.value = false;
  try {
    await userStore.updateProfile({
      ...userStore.user,
      email: data.email,
      newsletter_enabled: userStore.user?.newsletter_enabled ?? false,
    });
    isSuccess.value = true;
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Login failed";
    setError("root", { type: "manual", message });
  }
});
</script>

<template>
  <form @submit="onSubmit" class="space-y-4">
    <UiInput
      v-bind="register('email')"
      type="email"
      label="Email"
      placeholder="you@example.com"
      :error="formState.errors.email ? String(formState.errors.email) : undefined"
    />

    <p v-if="formState.errors.root" class="text-xs text-destructive">
      {{ formState.errors.root.message }}
    </p>

    <p v-if="isSuccess" class="text-xs text-green-500">
      Profile successfully updated
    </p>

    <UiButton
      type="submit"
      :disabled="isSubmitDisabled || emailValue === userStore.user?.email"
      :loading="formState.isSubmitting"
      class="w-full"
    >
      {{ formState.isSubmitting ? "Saving..." : "Save Changes" }}
    </UiButton>
  </form>
</template>
