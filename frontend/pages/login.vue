<template>
  <div class="w-full h-screen grid lg:grid-cols-2">
    <div class="flex items-center justify-center py-12">
      <div class="mx-auto w-[350px] space-y-6">
        <div class="text-center">
          <h1 class="text-3xl font-bold">Вход</h1>
          <p class="text-balance text-muted-foreground">
            Введите ваш email для входа в аккаунт
          </p>
        </div>

        <form @submit.prevent="onSubmit" class="space-y-4">
          <FormField
            name="email"
            v-slot="{ componentField }"
            :validate-on-blur="!isFieldDirty"
          >
            <FormItem v-auto-animate>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  v-bind="componentField"
                  required
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField
            name="password"
            v-slot="{ componentField }"
            :validate-on-blur="!isFieldDirty"
          >
            <FormItem v-auto-animate>
              <FormLabel>Пароль</FormLabel>
              <FormControl>
                <Input
                  id="password"
                  type="password"
                  v-bind="componentField"
                  required
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <Button type="submit" class="w-full">
            <span v-if="!isLoading">Войти</span>
            <div
              v-if="isLoading"
              class="animate-spin rounded-full h-5 w-5 border-b-2 border-secondary"
            ></div>
          </Button>
        </form>

        <div class="text-center text-sm">
          Нет аккаунта?
          <NuxtLink to="/signup" class="underline">Зарегистрироваться</NuxtLink>
        </div>
      </div>
    </div>

    <div class="hidden bg-muted lg:block">
      <img
        src="~/assets/img/med.png"
        alt="Image"
        width="1920"
        height="1080"
        class="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
      />
    </div>
  </div>
</template>

<script setup>
import { vAutoAnimate } from "@formkit/auto-animate/vue";

import { toTypedSchema } from "@vee-validate/zod";
import { useForm, useField } from "vee-validate";
import { h } from "vue";
import * as z from "zod";

// Схема валидации формы
const formSchema = toTypedSchema(
  z.object({
    email: z.string().email({ message: "Введите корректный email" }),
    password: z
      .string()
      .min(6, { message: "Пароль должен быть не менее 6 символов" }),
  })
);

const isLoading = ref(false);

// Форма
const { isFieldDirty, handleSubmit, setFieldError, setErrors } = useForm({
  validationSchema: formSchema,
});

const { login } = useSanctumAuth();

// Обработчик отправки формы
const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true;

  try {
    const response = await login(values);
  } catch (error) {
    setFieldError("password", error.data.message);
  } finally {
    isLoading.value = false; // Скрываем loader
  }
});
</script>

<style></style>
