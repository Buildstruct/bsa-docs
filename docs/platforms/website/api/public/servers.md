# {{ method("GET") }} /servers

`/api/public/servers`

Lists servers with optional search and pagination.\
Hidden servers are always excluded and the `hidden` field is not present in the response.\
Metadata follows the same visibility, so hidden servers never expose their `metadata` here.

For the private-layer variant (which exposes hidden servers and the `hidden` field), see [GET /api/private/servers](../private/servers.md).

## Query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | `string` | — | Partial name or metadata match (max 256 chars) |
| `order` | `created` \| `heartbeat` \| `name` | `created` | Sort column |
| `sorting` | `ascending` \| `DESC` | `DESC` | Sort direction |
| `limit` | `number` | `25` | Page size (capped by server config) |
| `page` | `number` | `0` | Zero-indexed page number |

## Response

`#!ts { servers[], count, page, limit }`

| Field | Type | Description |
|---|---|---|
| `server_id` | `number` | |
| `service_id` | `number` | |
| `name` | `string` | |
| `address` | `string \| null` | |
| `alive` | `0 \| 1` | `1` if heartbeat within the last 60 seconds, or `server_id = 1` |
| `created_at` | `string` | |
| `heartbeat_at` | `string` | |
| `player_count` | `number` | |
| `metadata` | `Record<string, string>` | Free-form server metadata, such as `map`, reported on heartbeat |
