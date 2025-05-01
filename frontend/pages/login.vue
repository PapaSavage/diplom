<template>
  <div class="w-full h-screen grid lg:grid-cols-2">
    <div class="flex items-center justify-center py-12">
      <div class="mx-auto grid w-[350px] gap-6">
        <div class="grid gap-2 text-center">
          <h1 class="text-3xl font-bold">Вход</h1>
          <p class="text-balance text-muted-foreground">
            Введите ваш email для входа в аккаунт
          </p>
        </div>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="m@example.com"
              required
            />
          </div>
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Пароль</Label>
            </div>
            <Input id="password" type="password" required />
          </div>
          <Button type="submit" class="w-full"> Войти </Button>
        </div>
        <div class="text-center text-sm">
          Нет аккаунта?
          <a href="#" class="underline">
            <NuxtLink to="/signup">Зарегистрироваться</NuxtLink>
          </a>
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
<script lang="ts" setup></script>
<style></style>
