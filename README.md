# ContainerMesh

A macOS menu-bar app that discovers Docker containers and connects to them through ContainerTunnel. You choose which names to publish. Networking stays off until you choose **Enable automatic networking**.

Container and Compose-stack DNS names are optional. The usual name is the container plus `mesh.test`.

| Site | URL |
| --- | --- |
| Product home | https://www.containermesh.app/ |
| Documentation | https://www.containermesh.dev/docs/ |

This repository is the public site and the documentation.

## Issues and security

Public [Issues](https://github.com/Container-Mesh/site/issues) are for product bugs and for corrections to this site. Security reports stay private. Use the [security policy](SECURITY.md).

## Preview

```sh
python3 src/build.py
python3 -m http.server -d public
```

`python3 src/build.py --check` fails when `public/` does not match the sources, or when the copy picks up wording that does not belong on the public site.

## Publish

`main` builds with `python3 src/build.py` and deploys with Wrangler. The Worker serves both domains:

- `www.containermesh.app` is the product home. A docs path redirects to `www.containermesh.dev`.
- `www.containermesh.dev` is the documentation. `/` redirects to `/docs/`.
- The apex names redirect to `www`.

GitHub Actions also publishes `public/` to GitHub Pages as a preview.
