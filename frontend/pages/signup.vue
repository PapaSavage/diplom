<template>
  <div class="h-screen flex flex-col justify-center items-center">
    <Card class="max-w-sm mx-4">
      <CardHeader>
        <CardTitle class="text-xl">Регистрация</CardTitle>
        <CardDescription>
          Введите свои данные для создания аккаунта
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="submitForm" class="grid gap-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label for="first-name">Имя</Label>
              <Input
                v-model="formData.firstName"
                id="first-name"
                placeholder="Максим"
                required
              />
            </div>
            <div class="grid gap-2">
              <Label for="last-name">Фамилия</Label>
              <Input
                v-model="formData.lastName"
                id="last-name"
                placeholder="Петров"
                required
              />
            </div>
          </div>
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              v-model="formData.email"
              id="email"
              type="email"
              placeholder="m@example.com"
              required
            />
          </div>
          <div class="grid gap-2">
            <Label for="password">Пароль</Label>
            <Input
              v-model="formData.password"
              id="password"
              type="password"
              required
            />
          </div>
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
import { ref } from "#imports";
import { useFetch } from "#app";

const formData = ref({
  firstName: "",
  lastName: "",
  email: "",
  password: "",
});

async function submitForm() {
  try {
    const response = await useFetch("http://127.0.0.1:8000/api/register", {
      method: "POST",
      body: JSON.stringify({
        name: `${formData.value.firstName} ${formData.value.lastName}`,
        email: formData.value.email,
        password: formData.value.password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error(error);
  }
}
</script>
