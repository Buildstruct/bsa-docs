# API Reference

HTTP API exposed by the website backend.\
All endpoints are prefixed with `/api/`.

## Layers

| Layer | Base path | Auth required |
|---|---|---|
| Public | `/api/public/` | No |
| Private | `/api/private/` | Yes — Bearer token with `api.access` permission |

Most endpoints exist on both layers with identical behaviour.\
Exceptions are noted per-endpoint.\
The private layer exposes additional endpoints unavailable on public.

## Pagination

Paginated endpoints accept `limit` and `page` as query parameters.

| Parameter | Default | Notes |
|---|---|---|
| `limit` | `25` | Capped by server config per endpoint |
| `page` | `0` | Zero-indexed |

All paginated responses include `count`, `page`, and `limit` alongside the resource array.

## Ordering

Sortable endpoints accept `order` and `sorting` as query parameters.

| Parameter | Values | Default |
|---|---|---|
| `order` | Documented per endpoint | Endpoint default |
| `sorting` | `ascending`, `DESC` | `DESC` |

Unrecognised `order` values fall back to the endpoint's default.

---

## Endpoints

### Public layer

| Endpoint | Description |
|---|---|
| [GET /overview](public/overview.md) | Cached community snapshot (players, punishments, servers) |
| [GET /accounts](public/accounts.md) | Accounts — paginated, searchable |
| [GET /groups](public/groups.md) | All groups from cache |
| [GET /permissions](public/permissions.md) | All registered permissions from cache |
| [GET /providers](public/providers.md) | All providers from cache |
| [GET /punishments](public/punishments.md) | Punishments — paginated, filterable |
| [GET /servers](public/servers.md) | Servers — paginated, searchable, hidden servers excluded |
| [GET /services](public/services.md) | All services from cache |

### Private layer

Most public endpoints are also available at `/api/private/` with identical behaviour.\
The following are private-only or differ from their public counterpart.

| Endpoint | Description |
|---|---|
| [GET /servers](private/servers.md) | Same as public but includes `hidden` field, sessions with `management.interlink` can see hidden servers |
| [GET /commands](private/commands.md) | List all commands the authenticated player has permission to use |
| [POST /commands](private/commands.md) | Execute a command as the authenticated player |
