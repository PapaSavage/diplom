<template>
  <div>
    <patients-list />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import PatientsList from "@/components/PatientsList";

definePageMeta({
  layout: "admin",
});
</script>

<style scoped>
/* Дополнительные стили можно добавить здесь */
</style>
