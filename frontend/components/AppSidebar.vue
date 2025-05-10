<script setup>
import { useRoute } from "vue-router";
import { User, ChevronUp } from "lucide-vue-next";
import { toast } from "vue-sonner";

const props = defineProps(["items"]);

const route = useRoute();

const user = useSanctumUser();

const isActive = (url) => {
  return route.path === url;
};

const { $api } = useNuxtApp();

async function successLogout() {
  const tokenCookie = useCookie("sanctum.token.cookie");
  tokenCookie.value = null;

  // Очищаем пользователя (если нужно)
  user.value = null;

  toast("Вы успешно вышли из аккаунта", {
    description: "Сейчас мы вас переадресуем на страницу авторизации",
  });

  await navigateTo("/login");
}

async function logout(data) {
  try {
    const response = await $api("/logout", {
      method: "POST",
      onResponse: ({ response }) => {
        if ([200, 201].includes(response.status)) {
          successLogout();
        }
      },
    });
  } catch (error) {}
}
</script>

<template>
  <Sidebar>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>МедВизор</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in items" :key="item.title">
              <SidebarMenuButton
                asChild
                :class="{ 'bg-gray-200': isActive(item.url) }"
              >
                <NuxtLink :to="item.url">
                  <component :is="item.icon" />
                  <span>{{ item.title }}</span>
                </NuxtLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuButton>
                <User />
                <span class="text-sm">
                  {{ user.name }}
                </span>
                <ChevronUp class="ml-auto" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              side="top"
              class="w-[--reka-popper-anchor-width]"
            >
              <DropdownMenuItem>
                <span>Аккаунт</span>
              </DropdownMenuItem>

              <DropdownMenuItem @click="logout">
                <span>Выйти</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter></Sidebar
  >
</template>
