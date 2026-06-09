# {{ method("GET") }} /providers

`/api/public/providers` · `/api/private/providers`

Returns all providers from cache.\
Behaviour is identical on both layers.

!!! note
    Returns a plain array, not a wrapped object.

## Response

`#!ts { provider_id, name, alias }[]`

| Field | Type |
|---|---|
| `provider_id` | `number` |
| `name` | `string` |
| `alias` | `string` |
