# {{ method("GET") }} /accounts

`/api/public/accounts` · `/api/private/accounts`

Lists accounts with optional search and pagination.\
Behaviour is identical on both layers.

## Query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `search` | `string` | — | Exact identifier match or partial username match (max 256 chars) |
| `order` | `created` \| `username` \| `time` | `created` | Sort column |
| `sorting` | `ascending` \| `DESC` | `DESC` | Sort direction |
| `limit` | `number` | `25` | Page size (capped by server config) |
| `page` | `number` | `0` | Zero-indexed page number |

## Response

`#!ts { accounts[], count, page, limit }`

| Field | Type |
|---|---|
| `account_id` | `number` |
| `player_id` | `number` |
| `group_id` | `number` |
| `secondary_groups` | `number[]` |
| `provider_id` | `number` |
| `identifier` | `string` |
| `username` | `string \| null` |
| `time` | `number` |
| `created_at` | `string` |
