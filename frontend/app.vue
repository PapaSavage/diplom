<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.4s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}

/* Анимация перехода между layout'ами */
.layout-enter-active,
.layout-leave-active {
  transition: all 0.4s ease;
}
.layout-enter-from,
.layout-leave-to {
  opacity: 0;
  filter: grayscale(1);
}
</style>
