# {{ method("GET") }} /overview

`/api/public/overview`

Returns a cached community snapshot. Results are cached for 60 seconds.

## Response

```json
{
  "players": {
    "total":      0,
    "online":     0,
    "joined_7d":  0,
    "joined_30d": 0
  },
  "punishments": {
    "active_ban":     0,
    "active_warn":    0,
    "active_silence": 0
  },
  "servers": [
    { "name": "string", "alive": false }
  ],
  "retention": {
    "active_7d":  0,
    "active_30d": 0,
    "rate":       0
  },
  "cached_at": "ISO 8601 timestamp"
}
```

| Field | Description |
|---|---|
| `players.total` | Total registered players (excludes reserved system rows) |
| `players.online` | Players with an active session heartbeat in the last 60 seconds |
| `players.joined_7d` / `joined_30d` | New players in the last 7 or 30 days |
| `punishments.active_ban` | Active bans |
| `punishments.active_warn` | Active warns |
| `punishments.active_silence` | Active mutes, gags, or similar silence types |
| `servers` | All non-hidden servers with their alive state |
| `retention.rate` | Percentage of 30-day active players who were also active in the last 7 days |
| `cached_at` | When this snapshot was last built |
