export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    if (path.startsWith('/api/')) {
      // Preserve URL, Origin, Cookie and result credentials for same-origin auth.
      // This is a service binding, never a public workers.dev HTTP request.
      return env.BACKEND.fetch(request);
    }
    return env.ASSETS.fetch(request);
  }
};
