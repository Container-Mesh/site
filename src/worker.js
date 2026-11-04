export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();
    if (host === "containermesh.app" || host === "containermesh.dev") {
      url.hostname = "www." + host;
      return Response.redirect(url.toString(), 308);
    }
    if (host === "www.containermesh.dev" && (url.pathname === "/" || url.pathname === "/index.html")) {
      url.pathname = "/docs/";
      return Response.redirect(url.toString(), 302);
    }
    if (host === "www.containermesh.app" && (url.pathname === "/docs" || url.pathname.startsWith("/docs/"))) {
      const dest = new URL("https://www.containermesh.dev");
      dest.pathname = url.pathname;
      dest.search = url.search;
      return Response.redirect(dest.toString(), 302);
    }
    return env.ASSETS.fetch(request);
  }
}
