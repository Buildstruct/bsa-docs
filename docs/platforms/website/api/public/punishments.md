# {{ method("GET") }} /punishments

`/api/public/punishments` · `/api/private/punishments`

Lists punishments with optional filtering and pagination.\
Behaviour is identical on both layers.

## Query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | `string` | — | Matches any identifier or username associated with the punished player (max 256 chars) |
| `type` | `string` | — | Filter by punishment type string; omit or pass `all` for no filter |
| `active` | `active` \| `inactive` \| `any` | `any` | Filter by active state |
| `order` | `created` \| `username` \| `expires` | `created` | Sort column |
| `sorting` | `ascending` \| `DESC` | `DESC` | Sort direction |
| `limit` | `number` | `25` | Page size (capped by server config) |
| `page` | `number` | `0` | Zero-indexed page number |

## Response

`#!ts { punishments[], count, page, limit }`

| Field | Type | Description |
|---|---|---|
| `punishment_id` | `number` | |
| `type` | `string` | |
| `active` | `0 \| 1` | `1` if no revoker and not yet expired |
| `player_identifier` | `string` | Falls back to `#<player_id>` if no account row exists |
| `player_username` | `string \| null` | |
| `invoker_identifier` | `string` | |
| `invoker_username` | `string \| null` | |
| `revoker_identifier` | `string \| null` | |
| `revoker_username` | `string \| null` | |
| `reason` | `string \| null` | |
| `created_at` | `string` | |
| `expires_at` | `string \| null` | |
| `links` | `{ link_id, server_id, service_id, provider_id }[]` | Scope bindings |
