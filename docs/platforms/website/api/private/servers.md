# {{ method("GET") }} /servers

`/api/private/servers`

Lists servers with optional search and pagination.

Differs from the [public layer](../public/servers.md) in two ways:

- Each row includes a `hidden` field.
- Sessions with the `management.interlink` permission can see hidden servers.
  - Sessions without it see only non-hidden servers, same as the public layer.

## Query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | `string` | — | Partial name match (max 256 chars) |
| `order` | `created` \| `heartbeat` \| `name` | `created` | Sort column |
| `sorting` | `ascending` \| `DESC` | `DESC` | Sort direction |
| `limit` | `number` | `25` | Page size (capped by server config) |
| `page` | `number` | `0` | Zero-indexed page number |

## Response

`{ servers[], count, page, limit }`

| Field | Type | Description |
|---|---|---|
| `server_id` | `number` | |
| `service_id` | `number` | |
| `name` | `string` | |
| `address` | `string \| null` | |
| `hidden` | `0 \| 1` | `1` if the server is hidden from the public layer |
| `alive` | `0 \| 1` | `1` if heartbeat within the last 60 seconds, or `server_id = 1` |
| `created_at` | `string` | |
| `heartbeat_at` | `string` | |
