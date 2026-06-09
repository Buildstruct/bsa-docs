# {{ method("GET") }} /permissions

`/api/public/permissions` · `/api/private/permissions`

Returns all registered permissions from cache.\
Behaviour is identical on both layers.

## Response

`#!ts { permissions[] }`

| Field | Type |
|---|---|
| `perm_id` | `number` |
| `name` | `string` |
| `alias` | `string` |
