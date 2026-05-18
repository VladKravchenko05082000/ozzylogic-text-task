<script setup lang="ts">
import PageHeader from "@/components/PageHeader.vue";
import UiCard from "@/components/ui/UiCard.vue";
import ChangeUserDetailsForm from "./forms/ChangeUserDetailsForm.vue";
import ChangePasswordForm from "./forms/ChangePasswordForm.vue";
</script>

<template>
  <PageHeader title="Profile" description="Your account information" />

  <div class="flex flex-col gap-8">
    <UiCard class="p-5 space-y-4 max-w-md">
      <ChangeUserDetailsForm />
    </UiCard>

    <UiCard class="p-5 space-y-4 max-w-md">
      <ChangePasswordForm />
    </UiCard>
  </div>
</template>
