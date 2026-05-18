<script setup lang="ts">
import { computed, ref } from "vue";
import { useForm } from "@vuehookform/core";

import UiInput from "@/components/ui/UiInput.vue";
import UiButton from "@/components/ui/UiButton.vue";

import { changePasswordSchema } from "@/schemas/changePasswordSchema";
import { useUserStore, type ResetPasswordDataInterface } from "@/stores/userStore";

const { register, handleSubmit, formState, watch, setError } = useForm({
  schema: changePasswordSchema,
  defaultValues: {
    current_password: "",
    new_password: "",
  },
  mode: "onChange",
});

const userStore = useUserStore();
const isSuccess = ref(false);

const currentPasswordValue = watch("current_password");
const newPasswordValue = watch("new_password");

const isSubmitDisabled = computed(
  () =>
    formState.value.isSubmitting ||
    !currentPasswordValue.value ||
    !newPasswordValue.value ||
    !formState.value.isValid,
);

const onSubmit = handleSubmit(async (data: ResetPasswordDataInterface) => {
  isSuccess.value = false;
  try {
    await userStore.updatePassword(data);
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
      v-bind="register('current_password')"
      type="password"
      label="Current password"
      placeholder="Enter your current password"
      :error="
        formState.errors.current_password ? String(formState.errors.current_password) : undefined
      "
    />
    <UiInput
      v-bind="register('new_password')"
      type="password"
      label="New password"
      placeholder="Enter your disire new password"
    />

    <p v-if="formState.errors.new_password" class="text-xs text-destructive">
      {{ String(formState.errors.new_password) }}
    </p>

    <p v-if="formState.errors.root" class="text-xs text-destructive">
      {{ String(formState.errors.root) }}
    </p>

    <p v-if="isSuccess" class="text-xs text-green-500">
      Password successfully changed
    </p>

    <UiButton
      type="submit"
      :disabled="isSubmitDisabled"
      :loading="formState.isSubmitting"
      class="w-full"
    >
      {{ formState.isSubmitting ? "Saving..." : "Change Password" }}
    </UiButton>
  </form>
</template>
