<script setup lang="ts">
import { computed, ref } from "vue";

import { useForm } from "@vuehookform/core";

import PasswordEyeOpenIcon from "@/components/icons/password-eyes/PasswordEyeOpenIcon.vue";
import PasswordEyeCloseIcon from "@/components/icons/password-eyes/PasswordEyeCloseIcon.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UiButton from "@/components/ui/UiButton.vue";

import { authSchema } from "@/schemas/authSchema";

const { register, handleSubmit, formState, watch } = useForm({
  schema: authSchema,
  defaultValues: {
    email: "",
    password: "",
  },
});

const emailValue = watch("email");
const passwordValue = watch("password");

const showPassword = ref(false);

const isSubmitDisabled = computed(
  () =>
    formState.value.isSubmitting ||
    !emailValue.value ||
    !passwordValue.value ||
    !formState.value.isValid,
);

const onSubmit = handleSubmit((data) => {
  console.log("Login:", data);
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

    <div class="space-y-1.5">
      <label class="text-sm font-medium">Password</label>
      <div class="relative">
        <UiInput
          v-bind="register('password')"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Enter Your password"
          :error="formState.errors.password ? String(formState.errors.password) : undefined"
        />
        <button
          type="button"
          @click="showPassword = !showPassword"
          class="absolute right-2 top-4.5 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer z-10"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
        >
          <PasswordEyeOpenIcon v-if="!showPassword" />
          <PasswordEyeCloseIcon v-else />
        </button>
      </div>
    </div>

    <UiButton
      type="submit"
      variant="primary"
      :disabled="isSubmitDisabled"
      :loading="formState.isSubmitting"
      class="w-full"
    >
      {{ formState.isSubmitting ? "Signing in..." : "Sign In" }}
    </UiButton>
  </form>
</template>
