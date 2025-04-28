<template>
  <div class="h-screen flex flex-col justify-center items-center">
    <Card class="max-w-sm mx-4">
      <CardHeader>
        <CardTitle class="text-xl"> Регистрация </CardTitle>
        <CardDescription>
          Введите свои данные для создания аккаунта
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label for="first-name">Имя</Label>
              <Input id="first-name" placeholder="Максим" required />
            </div>
            <div class="grid gap-2">
              <Label for="last-name">Фамилия</Label>
              <Input id="last-name" placeholder="Петров" required />
            </div>
          </div>
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
            <Label for="password">Пароль</Label>
            <Input id="password" type="password" />
          </div>
          <Button type="submit" class="w-full"> Создать аккаунт </Button>
        </div>
        <div class="mt-4 text-center text-sm">
          Уже есть аккаунт?
          <a href="#" class="underline"> Войти </a>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
