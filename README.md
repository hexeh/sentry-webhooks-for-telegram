# Sentry Webhooks to Telegram
Since Sentry Cloud doesn't support Telegram integration, this sample project demonstrates such functionality

**Disclaimer**: not supposed to be used in production (look at todos and sqlite)

# Usage

1. Clone repo
2. Build docker image using provided Dockerfile
3. Run container with .env-file (look at sample.env)
4. Enable Sentry Webhook via Project Settings -> Legacy Integrations -> Webhooks -> Enable
5. Add Sentry webhook url as `https://{your_app_host}/v1/webhook/{project_id}`

TL;DR: Sentry project ID could be found from Settings -> Client Keys (DSN) as an end path for URL, i.e.
```sh
https://{sentry_secret}@{sentry_key}.ingest.sentry.io/{project_id}
```