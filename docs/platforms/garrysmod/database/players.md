# {{ realm("server") }} Players
Read/write interface for `bsa_players`, `bsa_accounts`, `bsa_player_groups`, and `bsa_addresses`.

!!! info
	See [core/database/tables/players.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/tables/players.lua) for the actual design implementation.\
	See [bsa_players](../../../database/tables/bsa_players.md) for player-based design requirements.\
	See [bsa_accounts](../../../database/tables/bsa_accounts.md) for account-based design requirements.\
	See [bsa_sessions](../../../database/tables/bsa_sessions.md) for session-based design requirements.\
	See [bsa_player_groups](../../../database/tables/bsa_player_groups.md) for secondary group design requirements.

## Functions

### Lookup

- `#!ts players:accounts(account: Player|string, callback?: function(data[] | false, secondaries[] | string))`\
  Finds accounts associated with a player, including secondary groups.\
  Calls back with account data, or `false` on error.

- `#!ts players:exists(account: Player|string, callback?: function(data | false, secondaries[] | string))`\
  Looks up an account row by the current provider + identifier (e.g.\
  SteamID64).\
  Calls back with account data and secondary group links, or `false` on not found.

- `#!ts players:exists_by_pid(player_id: number, callback?: function(data | false, secondaries[] | string))`\
  Same as `exists` but looks up by internal `player_id`.

- `#!ts players:exists_by_aid(account_id: number, callback?: function(data | false, secondaries[] | string))`\
  Same as `exists` but looks up by `account_id`.

### Connect + session

- `#!ts players:new(name: string, account: Player|string, callback?: function(data | false, secondaries[] | string))`\
  Finds or creates `bsa_players` and `bsa_accounts` rows for a player, then creates a session entry for the current server.\
  Used on player connect.

- `#!ts players:create_account(player_id: number, provider: string|number, identifier: string, username: string, callback?: function(data | false, secondaries[] | string))`\
  Creates a `bsa_accounts` row for an existing player, under the provider given by name or `provider_id`.\
  If the provider + identifier pair already exists on that player the username is refreshed and the row returned, if it belongs to another player the call fails.\
  Intended for linking external identities, such as Discord.

- `#!ts players:refresh(entity: Player, callback?: function(data | false, err?))`\
  Forces a full reload of a connected player's session and account data.\
  Intended for debugging — not for production use.

!!! warning
	`refresh` is for developer testing only.\
  Do not call it in normal flows.

- `#!ts players:heartbeat(account: Player|string, callback?: function())`\
  Updates `heartbeat_at` for the player's account row in the current provider.

- `#!ts players:attach(account: Player|string, callback?: function())`\
  Creates or updates a session row for the player on the current server.

- `#!ts players:detach(account: Player|string, callback?: function())`\
  Removes the player's session row for the current server.

### Time

- `#!ts players:settime(account: Player|string, time: number, callback?: function(data | false, err?))`\
  Writes a new playtime value to the database and updates the runtime `bsa_time` and `bsa_offset` variables for connected players.

### Groups

- `#!ts players:setprimary(account: Player|string, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Changes the player's primary group (`bsa_players.group_id`).\
  Fires an interlink command and updates runtime variables if the player is online.

- `#!ts players:setprimary_bypid(player_id: number, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Same as `setprimary` but targets by `player_id` instead of identifier.

- `#!ts players:addsecondary(account: Player|string, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Adds a secondary group row in `bsa_player_groups`.\
  Updates runtime `bsa_secondary` if the player is online.

- `#!ts players:addsecondary_bypid(player_id: number, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Same as `addsecondary` but targets by `player_id`.

- `#!ts players:removesecondary(account: Player|string, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Removes a secondary group row.\
  Updates runtime `bsa_secondary` if the player is online.

- `#!ts players:removesecondary_bypid(player_id: number, group_name: string|number, callback?: function(data | false, secondaries[] | string))`\
  Same as `removesecondary` but targets by `player_id`.

### Addresses

- `#!ts players:addresses(account: Player|string, callback?: function(rows | false))`\
  Returns all recorded IP addresses for the player's account from `bsa_addresses`, ordered by most recent.

- `#!ts players:record_address(account: Player|string, address: string)`\
  Inserts or updates an address entry in `bsa_addresses` for the player's account.\
  Called automatically on connect.

## Runtime Events
- `#!ts players.connected(invoker: Player)`
- `#!ts players.disconnected(invoker: Player)`
- `#!ts players.uconnected(account_data, secondaries)` — unknown/offline player connected (no live entity)
- `#!ts players.udisconnected(account_data, secondaries)` — unknown/offline player disconnected
- `#!ts players.timeset(account_data, time)`
- `#!ts players.primaryset(account_data, group, secondaries)`
- `#!ts players.secondaryadded(account_data, group, secondaries)`
- `#!ts players.secondaryremoved(account_data, group, secondaries)`

## Searcher Object
`players.searcher` is a query-builder for paginated player/account listings.

### Builder Methods
- `#!ts searcher:identifier(id: string|number): self`\
  Filters to a specific player by identifier or player_id.

- `#!ts searcher:provider(name_or_id: string|number): self`\
  Filters accounts by provider.

- `#!ts searcher:group(name_fragment: string): self`\
  Filters players whose primary or secondary group name/alias contains the fragment.

- `#!ts searcher:online(state: boolean): self`\
  Filters to players with or without an active session.

- `#!ts searcher:addresses(bool?: boolean): self`\
  When enabled, each row includes an `addresses` array from `bsa_addresses`.

- `#!ts searcher:sort_by_created()` / `sort_by_username()` / `sort_by_time()`
- `#!ts searcher:desc()` / `searcher:asc()`
- `#!ts searcher:page(limit: number, offset?: number): self`

- `#!ts searcher:query(callback: function(rows | false))`\
  Executes the query.\
  Each row includes `secondary` group links.\
  `rows.statistics.count` holds the total match count.

## References

- [Variables - Players](variables/players.md): Shared realm, replicated variables and player methods.
