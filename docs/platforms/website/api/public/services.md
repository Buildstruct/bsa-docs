# {{ method("GET") }} /services

`/api/public/services` · `/api/private/services`

Returns all services from cache.\
Behaviour is identical on both layers.

!!! note
    Returns a plain array, not a wrapped object.

## Response

`#!ts { service_id, provider_id, name, alias }[]`

| Field | Type |
|---|---|
| `service_id` | `number` |
| `provider_id` | `number` |
| `name` | `string` |
| `alias` | `string` |
