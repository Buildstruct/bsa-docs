# {{ method("GET") }} /userinfo

`/oauth/userinfo`

Returns the BSA identity behind an access token.\
The player's live ban state is checked on every call, a banned player's tokens are refused immediately.

## Request

```
Authorization: Bearer <access_token>
```

The response fields depend on the scopes granted with the token.\
`sub` is always present, everything else is scope gated.\
Permission names are the effective set from the player's groups (primary, secondary, and inherited), per-server permission targets are not exposed.

## Response

```json
{
	"sub": "12345",
	"username": "SomePlayer",
	"accounts": [
		{ "provider": "steam",   "identifier": "76561198000000000" },
		{ "provider": "discord", "identifier": "123456789012345678" }
	],
	"groups": [
		{ "name": "admin", "alias": "Admin", "weight": 100 }
	],
	"permissions": ["dashboard", "management.players", "kick"]
}
```

| Field | Scope | Description |
|---|---|---|
| `sub` | always | Stable BSA player id, as a string |
| `username` | `profile` | Current username, or `null` if none is set |
| `accounts` | `profile` | Every account linked to the player: provider name and identifier |
| `groups` | `groups` | BSA group memberships, sorted by weight descending |
| `permissions` | `permissions` | The player's effective permission names, resolved from their groups exactly like panel permission checks |

Only linked providers are listed, unlinked players cannot obtain tokens in the first place.

## Errors

| Status | Body | When |
|---|---|---|
| 401 | `{"error": "invalid_token"}` | Missing header, unknown/expired token, OAuth provider disabled, or banned player |
| 429 | (empty) | More than 120 calls per minute for the same token |

## Rate Limiting

120 requests per minute per token, then HTTP 429 with `Retry-After`.
