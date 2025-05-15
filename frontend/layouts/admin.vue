<template>
  <div>
    <SidebarProvider>
      <AppSidebar :items="items" />
      <SidebarInset>
        <header class="p-3 flex shrink-0 items-center gap-2 border-b">
          <SidebarTrigger />
          <Separator orientation="vertical" class="mr-2 h-3" />
          <div class="text-sm">{{ activeTitle }}</div>
        </header>
        <main class="p-4 w-full text-sm">
          <slot />
          <Toaster />
        </main>
      </SidebarInset>
    </SidebarProvider>
  </div>
</template>

<script setup>
import { Toaster } from "@/components/ui/sonner";
import AppSidebar from "@/components/AppSidebar.vue";
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import { Users, Stethoscope, Plus } from "lucide-vue-next";

const route = useRoute();

const activeTitle = computed(() => {
  const activeItem = items.value.find((item) => route.path === item.url);
  return activeItem ? activeItem.title : "Главная";
});

// Menu items.
const items = ref([
  {
    title: "Пациенты",
    url: "/patients",
    icon: Users,
  },
  {
    title: "Диагностика",
    url: "/diagnostics",
    icon: Stethoscope,
  },
  {
    title: "Новый случай",
    url: "/new-diagnostic",
    icon: Plus,
  },
]);
</script>

<style scoped>
/* Add any styles here if needed */
</style>
