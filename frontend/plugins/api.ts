export default defineNuxtPlugin((nuxtApp) => {
  // const { session } = useUserSession();
  const config = useRuntimeConfig();
  const api = $fetch.create({
    baseURL: config.public.apiBaseUrl as string,
    onRequest({ request, options, error }) {
      // if (session.value?.token) {
      //   options.headers.set("Authorization", `Bearer ${session.value?.token}`);
      // }
    },
    async onResponseError({ response }) {
      if (response.status === 401) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
    },
  });

  // Expose to useNuxtApp().$api
  return {
    provide: {
      api,
    },
  };
});
