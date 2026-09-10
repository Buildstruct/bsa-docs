# {{ method("GET") }} /.well-known/openid-configuration

`/.well-known/openid-configuration`

Discovery metadata so standard OAuth2/OIDC client libraries can auto-configure against BSA.\
`issuer` follows `baseline.web.url` when configured, otherwise the request host.

## Response

```json
{
	"issuer":                                "https://bsa.example.com",
	"authorization_endpoint":                "https://bsa.example.com/oauth/authorize",
	"token_endpoint":                        "https://bsa.example.com/oauth/token",
	"userinfo_endpoint":                     "https://bsa.example.com/oauth/userinfo",
	"scopes_supported":                      ["profile", "groups"],
	"response_types_supported":              ["code"],
	"grant_types_supported":                 ["authorization_code"],
	"code_challenge_methods_supported":      ["S256"],
	"token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"],
	"response_modes_supported":              ["query"]
}
```

## Errors

| Status | When |
|---|---|
| 404 | OAuth provider disabled |
