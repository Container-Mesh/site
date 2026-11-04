(function () {
  var address = String.fromCharCode(104, 101, 108, 108, 111, 64, 97, 112, 104, 101, 108, 105, 111, 110, 46, 119, 111, 114, 107, 115);
  document.querySelectorAll("a.contact").forEach(function (el) {
    el.textContent = address;
    el.href = "mailto:" + address;
  });
  var host = location.hostname.toLowerCase();
  var dev = host === "www.containermesh.dev" || host === "containermesh.dev";
  var app = host === "www.containermesh.app" || host === "containermesh.app";
  var path = location.pathname;
  if (dev && (path === "/" || path === "/index.html")) {
    location.replace("/docs/" + location.search + location.hash);
    return;
  }
  if (app && (path === "/docs" || path.indexOf("/docs/") === 0)) {
    location.replace("https://www.containermesh.dev" + path + location.search + location.hash);
    return;
  }
  if (!dev && !app) return;
  var docsOrigin = "https://www.containermesh.dev";
  var appOrigin = "https://www.containermesh.app";
  document.querySelectorAll("[data-docs-href]").forEach(function (el) {
    el.href = docsOrigin + el.getAttribute("data-docs-href");
  });
  document.querySelectorAll("[data-app-href]").forEach(function (el) {
    el.href = appOrigin + el.getAttribute("data-app-href");
  });
})();
