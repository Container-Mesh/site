export async function onRequest(context) {
  const url = new URL(context.request.url);
  const host = (context.request.headers.get("host") || "").replace(/:\d+$/, "").toLowerCase();
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
  return context.next();
}
