# {{ method("GET") }} /authorize

`/oauth/authorize`

Starts the OAuth 2.0 authorization code flow.\
The user is sent through the normal BSA login (Steam/Discord SSO) if they have no panel session, then shown a consent screen.

## Query Parameters

| Parameter | Required | Description |
|---|---|---|
| `response_type` | Yes | Must be `code` |
| `client_id` | Yes | The OAuth client id |
| `redirect_uri` | Yes | Must exact-match a URI registered on the client, `http(s)` only |
| `scope` | Yes | Space separated scopes, must be a subset of the client's registered scopes |
| `state` | Recommended | Echoed back to the redirect URI unchanged |
| `code_challenge` | Recommended | PKCE challenge (base64url SHA-256 of the verifier) |
| `code_challenge_method` | With `code_challenge` | Must be `S256` |

## Behaviour

1. Unknown or disabled client, or an unregistered `redirect_uri`: a plain error page is rendered. No redirect is performed.
2. Scope or protocol problems redirect back to the `redirect_uri` with the standard OAuth error and the original `state`:
	- `unsupported_response_type`
	- `invalid_scope` (unknown scope, or scope outside the client registration)
	- `invalid_request` (malformed PKCE parameters)
3. A banned or geoblocked player redirects back with `error=banned` or `error=geoblocked`.
4. Users without a BSA account linked to their upstream identity are refused, like panel logins.
5. If the player has a remembered grant covering the requested scopes, the code is issued immediately.
	Otherwise the consent screen is shown, then the code is issued on approval.
6. Denying consent redirects back with `error=access_denied`.

## Success Redirect

```
https://app.example.com/callback?code=<authorization_code>&state=<state>
```

| Field | Description |
|---|---|
| `code` | Single-use authorization code, expires in 60 seconds (configurable), bound to this client, redirect URI, and PKCE challenge |
| `state` | The value sent in the request |

## Errors

| Case | Behaviour |
|---|---|
| OAuth provider disabled | HTTP 403 error page |
| Unknown/disabled client, unregistered redirect URI | HTTP 400 error page (never redirects) |
| Rate limit exceeded | HTTP 429 (30 requests per minute per IP) |
