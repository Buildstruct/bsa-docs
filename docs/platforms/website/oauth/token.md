# {{ method("POST") }} /token

`/oauth/token`

Exchanges a single-use authorization code for an opaque access token.\
Called server-to-server by the third-party application, no browser or cookies involved.

## Request

`Content-Type: application/x-www-form-urlencoded`

| Parameter | Required | Description |
|---|---|---|
| `grant_type` | Yes | Must be `authorization_code` |
| `code` | Yes | The authorization code from the authorize redirect |
| `redirect_uri` | Yes | Must identical-match the one used in the authorize request |
| `code_verifier` | With PKCE | The plain text verifier matching the code's PKCE challenge |
| `client_id` / `client_secret` | Yes* | Client credentials in the body (if not sent via Basic auth) |

*Client authentication accepts HTTP Basic (`client_secret_basic`) or form body credentials (`client_secret_post`), matching the client's discovery metadata.

## Response

```json
{
	"access_token": "opaque token",
	"token_type":   "Bearer",
	"expires_in":   3600,
	"scope":        "profile groups"
}
```

| Field | Description |
|---|---|
| `access_token` | Opaque Bearer token for [GET /oauth/userinfo](userinfo.md) |
| `expires_in` | Token lifetime in seconds (`baseline.web.oauth.token_ttl`) |
| `scope` | Granted scopes |

## Errors

Per RFC 6749, returned as JSON with `Cache-Control: no-store`:

```json
{ "error": "invalid_grant", "error_description": "..." }
```

| Error | When |
|---|---|
| `invalid_client` (401) | Unknown client, disabled client, or wrong secret |
| `invalid_grant` | Code expired, already used, bound to another client, `redirect_uri` mismatch, or PKCE verification failed |
| `invalid_request` | Missing parameters or wrong content type |
| `unsupported_grant_type` | Anything other than `authorization_code` |
| `access_denied` | OAuth provider disabled |
| `server_error` (500) | Token could not be issued |

!!!warning
	A failed PKCE verification consumes the code.\
	This prevents brute-forcing the verifier from a leaked code.

## Rate Limiting

30 requests per minute per IP address, then HTTP 429 with `Retry-After`.
