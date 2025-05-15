<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white"
  >
    <!-- Основной контейнер -->
    <div class="container mx-auto px-4 py-12 max-w-6xl relative z-10">
      <!-- Заголовок -->

      <div class="min-h-screen flex flex-col align-items-center justify-center">
        <h1 class="text-4xl md:text-5xl font-extrabold mb-4 text-center">
          Диагностика заболеваний<br />на основе визуальных данных
        </h1>

        <p
          class="text-lg md:text-xl text-center text-gray-600 dark:text-gray-300 mb-8 mx-auto"
        >
          Современные технологии искусственного интеллекта позволяют создавать
          системы диагностики, которые помогают врачам быстрее и точнее выявлять
          заболевания по изображениям.
        </p>

        <!-- Кнопки -->
        <div class="flex justify-center gap-4 mb-12">
          <NuxtLink
            to="/login"
            class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-8"
          >
            Войти
          </NuxtLink>
          <NuxtLink
            to="/signup"
            class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-8"
          >
            Регистрация
          </NuxtLink>
        </div>
      </div>

      <!-- Карточки -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <h1
          class="text-2xl md:text-3xl font-extrabold mb-4 text-center col-span-2"
        >
          Диагностика заболеваний по изображениям — ИИ в медицине
        </h1>

        <!-- Функциональная карточка -->
        <Card class="shadow-lg">
          <CardHeader>
            <CardTitle>Как это работает</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <p>
              Наше приложение использует современные модели искусственного
              интеллекта для анализа медицинских изображений. Пациент загружает
              фото (например, кожи, глаз, рентгеновского снимка), система
              автоматически обрабатывает его и выдает предварительный результат.
            </p>
            <ul class="list-disc pl-5 space-y-2">
              <li>
                <strong>Загрузите изображение:</strong> Выберите файл
                изображения пациента.
              </li>
              <li>
                <strong>Анализ данных:</strong> ИИ анализирует структуру, цвет,
                форму и другие параметры.
              </li>
              <li>
                <strong>Результат:</strong> Получите рекомендации или
                предварительный диагноз, который можно обсудить с лечащим
                врачом.
              </li>
            </ul>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
              Система не заменяет врача, а служит вспомогательным инструментом.
            </p>
          </CardContent>
        </Card>

        <!-- Для кого полезно -->
        <Card class="shadow-lg">
          <CardHeader>
            <CardTitle>Для кого это приложение?</CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <p>
              Приложение подходит как для пациентов, так и для медицинского
              персонала. Оно помогает быстро получить информацию о возможных
              изменениях на коже, ранних признаках болезней и других состояниях.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-md">
                <h3 class="font-semibold">Врачи</h3>
                <p>
                  Ускорьте процесс диагностики, получайте дополнительную
                  информацию перед осмотром и повышайте точность постановки
                  диагноза.
                </p>
              </div>
              <div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-md">
                <h3 class="font-semibold">Пациенты</h3>
                <p>
                  Самостоятельно отслеживайте состояние своего здоровья,
                  отправляйте изображения своему врачу и получайте рекомендации
                  в режиме реального времени.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Преимущества -->
      <Card class="mt-12 shadow-lg">
        <CardHeader>
          <CardTitle>Почему стоит использовать?</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <p>
            Наше решение объединяет современные технологии искусственного
            интеллекта и медицинскую экспертизу. Вот основные преимущества:
          </p>
          <ul class="list-disc pl-5 space-y-2">
            <li>
              <strong>Быстрая диагностика:</strong> Анализ изображения занимает
              всего несколько секунд.
            </li>
            <li>
              <strong>Высокая точность:</strong> Модели ИИ обучены на миллионах
              клинических случаев.
            </li>
            <li>
              <strong>Простота использования:</strong> Не требует специальных
              знаний — удобно как для пациентов, так и для врачей.
            </li>
            <li>
              <strong>Поддержка разных типов изображений:</strong> Работает с
              фото кожи, глаз, рентгеновскими снимками и другими медицинскими
              данными.
            </li>
            <li>
              <strong>Конфиденциальность:</strong> Все данные защищены,
              соблюдается конфиденциальность и безопасность.
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>

    <!-- Фоновое изображение -->
    <div class="fixed inset-0 opacity-5">
      <img
        src="~/assets/img/index_background.webp"
        alt="Medical AI Background"
        class="w-full h-full object-cover"
        loading="lazy"
      />
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "default",
  sanctum: {
    guestOnly: true,
  },
});
</script>
