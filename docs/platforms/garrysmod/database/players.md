# Players
Read/write interface for `bsa_players`, `bsa_accounts`, and `bsa_player_groups` membership updates, plus account heartbeat/time synchronization.

## Functions
- `#!ts players:exists_by_pid(player_id: number, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Looks up account/player state by internal `player_id`.

- `#!ts players:exists(account: Player|string, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Looks up by current provider + identifier (e.g. SteamID64).

- `#!ts players:new(name: string, account: Player|string, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Finds or creates account/player rows and attaches to current server.

- `#!ts players:settime(account: Player|string, time: number, callback?: function(account_data|false, err?: string))`\
Persists playtime and updates runtime variables (`bsa_offset`, `bsa_time`) for online targets.

- `#!ts players:heartbeat(account: Player|string, callback?: function())`\
Writes `heartbeat_at` for account in current provider.

- `#!ts players:attach(account: Player|string, callback?: function())`\
Sets account `server_id` + heartbeat to current server.

- `#!ts players:detach(account: Player|string, callback?: function())`\
Clears account `server_id` + updates heartbeat.

- `#!ts players:setprimary(account: Player|string, group_name: string|number, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Changes primary group assignment (`bsa_players.group_id`).

- `#!ts players:addsecondary(account: Player|string, group_name: string|number, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Adds secondary group row in `bsa_player_groups` and updates runtime `bsa_secondary` if player is online.

- `#!ts players:removesecondary(account: Player|string, group_name: string|number, callback?: function(account_data|false, secondaries?: table, err?: string))`\
Removes secondary group assignment and updates runtime `bsa_secondary` if player is online.

## Runtime Events
- `#!ts players.connected(invoker: Player)`
- `#!ts players.disconnected(invoker: Player)`
- `#!ts players.uconnected(account_data, secondaries)`
- `#!ts players.udisconnected(account_data, secondaries)`
- `#!ts players.timeset(account_data, time)`
- `#!ts players.primaryset(account_data, group, secondaries)`
- `#!ts players.secondaryadded(account_data, group, secondaries)`
- `#!ts players.secondaryremoved(account_data, group, secondaries)`

## Searcher Object
`players.searcher` is a query-builder class for paginated player/account listings.

### Builder Methods
- `#!ts players.searcher:identifier(id: string|number): self`
- `#!ts players.searcher:provider(name_or_id: string|number): self`
- `#!ts players.searcher:group(name_fragment: string): self`
- `#!ts players.searcher:online(state: boolean): self`
- `#!ts players.searcher:sort_by_created()`
- `#!ts players.searcher:sort_by_username()`
- `#!ts players.searcher:sort_by_time()`
- `#!ts players.searcher:desc()`
- `#!ts players.searcher:asc()`
- `#!ts players.searcher:page(limit: number, offset?: number): self`
- `#!ts players.searcher:query(callback: function(rows|false))`\
Executes query and returns rows with `rows.statistics.count` and per-row `secondary` group links.

## References

- [Variables - Players](variables/players.md): Shared realm, networked information and player functions.