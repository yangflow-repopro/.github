<!-- template: website/README.md v1 -->
<!-- Website README. Replace every <...>. Six H2s in this order. -->
# <Name> website

Static website of <Name> (`https://<domain>`), nine languages, deployed as Cloudflare Workers static assets
from `public/`.

## Deploy

<How the site is deployed (Git integration, build command, domain binding). Includes: workers.dev and preview
URLs are off.>

## Work on it

<The five commands in order (check_i18n, build, diff, check_site, check_facts) and the preview command.
Edit `i18n/*.json`, never the generated HTML. Commit generated files with the source change.>

## Pages

<Table: page, address, source of its copy. Every page has exactly one address.>

## Languages

<Link `handbook/localization.md`; how to add a language here.>

## Content sources

<Where each kind of content comes from: the app's `docs/legal.md` for facts, `changelog.json` written by the app's script, screenshots from the app's export script.>

## App dependencies

<The paths and feeds the app relies on (stable): `/`, `/terms`, `/privacy`, `/changelog`, `https://dl.<domain>/latest.json`.>
