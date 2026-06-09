# {{ method("GET") }} /groups

`/api/public/groups` · `/api/private/groups`

Returns all groups from cache.\
Behaviour is identical on both layers.

## Response

`#!ts { groups[] }`

| Field | Type | Description |
|---|---|---|
| `group_id` | `number` | |
| `name` | `string` | |
| `alias` | `string` | |
| `color` | `string` | |
| `weight` | `number` | |
| `inherit_id` | `number \| null` | Direct parent group, or `null` |
| `inheritances` | `number[]` | Flat list of all ancestor group IDs, ordered from closest to furthest |
| `links` | `Link[]` | Scope bindings |
| `permissions` | `Permission[]` | |

#### Link

| Field | Type |
|---|---|
| `link_id` | `number` |
| `provider_id` | `number \| null` |
| `service_id` | `number \| null` |
| `server_id` | `number \| null` |

#### Permission

| Field | Type | Description |
|---|---|---|
| `name` | `string` | Permission name (e.g. `punishments.ban`) |
| `scopes` | `Scope[]` | Scopes the permission applies to |

#### Scope

| Field | Type |
|---|---|
| `provider_id` | `number \| null` |
| `service_id` | `number \| null` |
| `server_id` | `number \| null` |
