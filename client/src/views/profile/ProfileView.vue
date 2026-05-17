<script setup lang="ts">
import { computed } from "vue";
import { useForm } from "@vuehookform/core";

import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import UiInput from "@/components/ui/UiInput.vue";
import UiButton from "@/components/ui/UiButton.vue";

import { profileSchema } from "@/schemas/profileSchema";

const { register, handleSubmit, formState, watch } = useForm({
  schema: profileSchema,
  defaultValues: {
    email: "",
  },
});

const emailValue = watch("email");

const isSubmitDisabled = computed(
  () => formState.value.isSubmitting || !emailValue.value || !formState.value.isValid,
);

const onSubmit = handleSubmit(async (data) => {
  console.log("Update profile:", data);
});
</script>

<template>
  <PageHeader title="Profile" description="Your account information" />

  <UiCard class="p-5 space-y-4 max-w-md">
    <form @submit="onSubmit" class="space-y-4">
      <UiInput
        v-bind="register('email')"
        type="email"
        label="Email"
        placeholder="you@example.com"
        :error="formState.errors.email ? String(formState.errors.email) : undefined"
      />

      <UiButton
        type="submit"
        :disabled="isSubmitDisabled"
        :loading="formState.isSubmitting"
        class="w-full"
      >
        {{ formState.isSubmitting ? "Saving..." : "Save Changes" }}
      </UiButton>
    </form>
  </UiCard>
</template>
