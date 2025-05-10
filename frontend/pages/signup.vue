<template>
  <div class="h-screen flex flex-col justify-center items-center">
    <Card class="max-w-sm mx-4 w-full">
      <CardHeader>
        <CardTitle class="text-xl">Регистрация</CardTitle>
        <CardDescription
          >Введите свои данные для создания аккаунта</CardDescription
        >
      </CardHeader>
      <CardContent>
        <form @submit="onSubmit" class="space-y-4">
          <FormField
            name="firstName"
            v-slot="{ componentField }"
            :validate-on-blur="!isFieldDirty"
          >
            <FormItem v-auto-animate>
              <FormLabel>Имя</FormLabel>
              <FormControl>
                <Input
                  id="first-name"
                  placeholder="Максим"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField
            name="lastName"
            v-slot="{ componentField }"
            :validate-on-blur="!isFieldDirty"
          >
            <FormItem v-auto-animate>
              <FormLabel>Фамилия</FormLabel>
              <FormControl>
                <Input
                  id="last-name"
                  placeholder="Петров"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

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
                  type="text"
                  placeholder="m@example.com"
                  v-bind="componentField"
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
                <Input id="password" type="text" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <Button type="submit" class="w-full">
            <span v-if="!isLoading"> Создать аккаунт </span>
            <div
              v-if="isLoading"
              class="animate-spin rounded-full h-5 w-5 border-b-2 border-secondary"
            ></div>
          </Button>
        </form>

        <div class="mt-4 text-center text-sm">
          Уже есть аккаунт?
          <NuxtLink to="/login" class="underline">Войти</NuxtLink>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { vAutoAnimate } from "@formkit/auto-animate/vue";

import { toTypedSchema } from "@vee-validate/zod";
import { useForm, useSetFieldError } from "vee-validate";
import * as z from "zod";
import { toast } from "vue-sonner";

definePageMeta({
  sanctum: {
    guestOnly: true,
  },
});

// Схема валидации формы
const formSchema = toTypedSchema(
  z.object({
    firstName: z
      .string()
      .min(2, { message: "Имя должно быть не короче 2 символов" }),
    lastName: z
      .string()
      .min(2, { message: "Фамилия должна быть не короче 2 символов" }),
    email: z.string().email({ message: "Введите корректный email" }),
    password: z
      .string()
      .min(6, { message: "Пароль должен быть не менее 6 символов" }),
  })
);

// Форма
const { isFieldDirty, handleSubmit, setFieldError, setErrors } = useForm({
  validationSchema: formSchema,
});

// Обработчик отправки формы
const onSubmit = handleSubmit((values) => {
  registerUser(values);
});

const { $api } = useNuxtApp();

const isLoading = ref(false);

async function successRegistration() {
  toast("Вы успешно зарегистрировались", {
    description: "Сейчас мы вас переадресуем на страницу авторизации",
  });

  await navigateTo("/login");
}

async function registerUser(data) {
  isLoading.value = true;
  try {
    const response = await $api("/register", {
      method: "POST",
      body: JSON.stringify({
        name: `${data.firstName} ${data.lastName}`,
        email: data.email,
        password: data.password,
      }),
      onResponse: ({ response }) => {
        if ([200, 201].includes(response.status)) {
          successRegistration();
        }
      },
    });
  } catch (error) {
    handleApiErrors(error.data?.errors);
  } finally {
    isLoading.value = false; // Скрываем loader
  }
}

function handleApiErrors(errors) {
  setErrors(errors);
}
</script>
