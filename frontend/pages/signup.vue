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

          <Button type="submit" class="w-full">Создать аккаунт</Button>
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

async function registerUser(data) {
  try {
    const response = await $api("/register", {
      method: "POST",
      body: JSON.stringify({
        name: `${data.firstName} ${data.lastName}`,
        email: data.email,
        password: data.password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Если регистрация успешна
    if (response.status === 201 || response.status === 200) {
      alert("Регистрация прошла успешно!");
      // Например, редирект на /login
      return true;
    }

    // Обработка ошибок, если статус не 200-201
    const errorData = await response.json();
    throw new Error(JSON.stringify(errorData));
  } catch (error) {
    handleApiErrors(error.data?.errors);
  }
}

function handleApiErrors(errors) {
  setErrors(errors);
  // for (const field in errors) {

  //   const message = errors[field][0];
  //   useSetFieldError(field, message);
  // }
}
</script>
