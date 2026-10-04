# Releases (websites)

A website is deployed from `main` on every merge; it is not tagged.

## Deploy

Cloudflare's Git integration deploys `main` with `npx wrangler deploy` and an empty build command.
`workers_dev` and `preview_urls` are off; the custom domain is bound in the dashboard. After a repository
transfer the Git connection must be re-authorized in the dashboard.
