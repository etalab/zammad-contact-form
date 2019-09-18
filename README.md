# zammad-contact-form

## Quickstart

Build locally:

```
now dev
```

Deploy

```
now
```

## Configuration

Relies on `Z_TOKEN` env var being set with a valid Zammad API token. On now, `z-token` [secret should be set ](https://zeit.co/docs/v2/serverless-functions/env-and-secrets/#adding-secrets). Locally, `.env` is used with `Z_TOKEN=xxx`.

Zammad URL is stored in `api/index.py::BASE_URL`.
