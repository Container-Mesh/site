# ContainerMesh site

Public product home and documentation for ContainerMesh. This repository does not contain the application.

| Site | URL |
| --- | --- |
| Product home | https://www.containermesh.app/ |
| Documentation | https://www.containermesh.dev/docs/ |

ContainerMesh is a macOS menu-bar app. It discovers Docker containers and connects to them through ContainerTunnel. Container and Compose-stack DNS names are optional. Prerequisite checks come first. Automatic connection starts only after **Enable automatic networking**.

## Issues and security

Public [Issues](https://github.com/Container-Mesh/site/issues) are for product bugs and for corrections to this site. Security reports stay private. Use the [security policy](SECURITY.md). Do not open a public issue for a vulnerability.

## Preview

```sh
python3 src/build.py
python3 -m http.server -d public
```

`python3 src/build.py --check` fails when `public/` does not match the sources, or when the copy picks up wording that does not belong on the public site.

## Publish

The site is one static tree in `public/`. GitHub Actions publishes that tree to GitHub Pages. GitHub Pages serves one certificate name, so both product domains belong on a host that can attach `www.containermesh.app` and `www.containermesh.dev` to the same files.

On Cloudflare Pages, the build command is `python3 src/build.py` and the output directory is `public`. `functions/_middleware.js` sends each domain to its own pages:

- `www.containermesh.app` is the product home. A docs path redirects to `www.containermesh.dev`.
- `www.containermesh.dev` is the documentation. `/` redirects to `/docs/`.
- The apex names redirect to `www`.

Point both `www` names at that host. The pages also rewrite those links in the browser when the pages host is one of the two domains, so a static server without the middleware still separates them.

The Snapfit mark and the orange app icon in `src/assets/` are the public artwork. Orange runs from `#FF941F` to `#B8360B`. The mark is `#FFF4DD`.
