export default defineNuxtPlugin((nuxtApp) => {
  // const { session } = useUserSession();

  function getAuthTokenFromCookie() {
    const cookie = useCookie("sanctum.token.cookie");
    return cookie.value;
  }

  const config = useRuntimeConfig();
  const api = $fetch.create({
    baseURL: config.public.apiBaseUrl as string,
    onRequest({ request, options, error }) {
      const token = getAuthTokenFromCookie();

      if (token) {
        options.headers.set("Authorization", `Bearer ${token}`);
      }
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
