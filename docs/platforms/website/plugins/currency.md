# {{ state("private") }} Currency
Dynamic, multi-type currency management with arbitrary-precision values.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

---

## Value format

All balance values are returned in three forms:

| Field | Example | Description |
|---|---|---|
| `value` | `"1500000"` | Exact decimal string |
| `named` | `"1.5 Million"` | Human-readable long form |
| `short_named` | `"1.5M"` | Abbreviated form |

The `inflation` endpoint also includes `exponential` (e.g. `"1.5e7"`).

---

## API Endpoints

The `types`, `inflation`, and `top` endpoints are available on all three layers.\
The `get` and `player` endpoints are panel-only (session + `management.currency` required).

!!! note
	Public and private API availability is togglable per-endpoint via the configurate system under `plugins.currency`.

### {{ method("GET") }} /currency/types

`/api/plugin/currency/types` · `/api/public/currency/types` · `/api/private/currency/types`

Returns all currency types known to the website. Cached — refreshed every 5 seconds on access.

#### Response

```json
{
  "types": [
    { "tag": "gear", "alias": "Gear" }
  ]
}
```

---

### {{ method("GET") }} /currency/inflation

`/api/plugin/currency/inflation` · `/api/public/currency/inflation` · `/api/private/currency/inflation`

Returns the total amount of a currency type held across all players.

#### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `type` | Yes | Currency type tag (e.g. `gear`) |

#### Response

```json
{
  "type":        "gear",
  "inflation":   "15000000",
  "exponential": "1.5e7",
  "named":       "15 Million",
  "short_named": "15M"
}
```

---

### {{ method("GET") }} /currency/top

`/api/plugin/currency/top` · `/api/public/currency/top` · `/api/private/currency/top`

Returns the top holders of a currency type ordered by balance, highest first.

#### Query parameters

| Parameter | Default | Description |
|---|---|---|
| `type` | — (required) | Currency type tag |
| `limit` | `10` | Number of rows (capped by `leaderboard_limit` config, default 25) |

#### Response

Each entry includes all accounts linked to that player — there may be more than one if the player has connected through multiple platforms.

```json
{
  "type": "gear",
  "rows": [
    {
      "player_id":   42,
      "accounts": [
        { "account_id": 1, "provider_id": 2, "identifier": "76561198000000000", "username": "BlueShank" },
        { "account_id": 5, "provider_id": 4, "identifier": "123456789",         "username": "BlueShank" }
      ],
      "value":       "5000000",
      "named":       "5 Million",
      "short_named": "5M"
    }
  ]
}
```

---

### {{ method("GET") }} /currency/get

`/api/plugin/currency/get` — panel only

Returns the balance of a single player for a specific currency type.

#### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `player_id` | Yes | Internal `player_id` |
| `type` | Yes | Currency type tag |

#### Response

Returns zero values if the player has no record for that type.

```json
{
  "player_id":  42,
  "type":       "gear",
  "value":      "250",
  "named":      "250",
  "short_named":"250",
  "updated_at": "2026-01-01T00:00:00.000000Z"
}
```

---

### {{ method("GET") }} /currency/player

`/api/plugin/currency/player` — panel only

Returns all currency balances for a player across all registered types.

#### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `q` | Yes | Player identity — `UID:<player_id>`, `ACC:<account_id>`, `<provider>:<identifier>`, or raw identifier |

#### Response

`accounts` contains all platform accounts linked to this player.

```json
{
  "player_id": 42,
  "accounts": [
    { "account_id": 1, "provider_id": 2, "identifier": "76561198000000000", "username": "BlueShank" },
    { "account_id": 5, "provider_id": 4, "identifier": "123456789",         "username": "BlueShank" }
  ],
  "balances": [
    {
      "type":        "gear",
      "meta":        { "tag": "gear", "alias": "Gear" },
      "value":       "250",
      "named":       "250",
      "short_named": "250",
      "updated_at":  "2026-01-01T00:00:00.000000Z"
    }
  ]
}
```