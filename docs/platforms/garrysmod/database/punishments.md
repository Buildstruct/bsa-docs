# {{ realm("server") }} Punishments
Read/write interface for `bsa_punishments` with scoped replication, active-cache management, and periodic expiration invalidation.

!!! info
	See [core/database/tables/punishments.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/tables/punishments.lua) for the actual design implementation.\
	See [bsa_punishments](../../../database/tables/bsa_punishments.md) for implementation & design requirements.

## Functions
- `#!ts punishments:add(target: Player|string, invoker: Player|string, type: string, duration?: number, reason: string, callback?: function(entry|false, err?: string), hidden?: boolean)`\
	Creates a punishment in current provider/service/server scope.\
	`hidden` (trailing the callback) marks the punishment as hidden from non-privileged views.

- `#!ts punishments:addex(target: Player|string, invoker: Player|string, type: string, duration?: number, reason: string, scopes: table, callback?: function(entry|false, err?: string), hidden?: boolean)`\
	Creates punishment with explicit scopes.\
	`scopes` is a list of `{provider_id: number?, service_id: number?, server_id: number?}` tables, each entry becomes one row in `bsa_punishment_links`.\
	Fails with `"no scopes provided"` if empty. `hidden` is the trailing boolean.

- `#!ts punishments:revoke(id: number, revoker: Player|string, callback?: function(entry|false, err?: string))`\
	Sets `revoker_id` and removes active entry from local identifier cache.

- `#!ts punishments:remove(id: number, callback?: function(entry|false, err?: string))`\
	Hard-deletes punishment row.

- `#!ts punishments:exist_by_id(id: number, callback?: function(entry|false, err?: string))`\
	Fetches one punishment by `punishment_id`.

- `#!ts punishments:exist(identifier: string, callback?: function(entries|false, err?: string))`\
	Fetches all punishments for identifier filtered by current scope.

- `#!ts punishments:active(identifier: string, callback?: function(entries|false, err?: string))`\
	Fetches only currently active punishments for identifier filtered by current scope.

- `#!ts punishments:rereason(id: number, new_reason: string, callback?: function(entry|false, err?: string))`\
	Updates reason and refreshes cached row copy.

- `#!ts punishments:reduration(id: number, new_duration?: number, callback?: function(entry|false, err?: string))`\
	Updates duration (`NULL` for permanent) and re-sorts cached entries.

- `#!ts punishments:rehidden(id: number, new_hidden: boolean, callback?: function(entry|false, err?: string))`\
	Toggles the `hidden` flag and patches the cached row.\
	Broadcasts `database.punishments:update`.

- `#!ts punishments:rescope(id: number, scope: table, callback?: function(entry|false, err?: string))`\
	Replaces the punishment's scope links with a single `{provider_id?, service_id?, server_id?}` scope.\
	Broadcasts `database.punishments:rescope`.

- `#!ts punishments:scope_add(id: number, scope: table, callback?: function(entry|false, err?: string))`\
	Adds one scope link.\
	Fails with `"scope link already exists"` if the link is a duplicate. Broadcasts `database.punishments:scope_added`.

- `#!ts punishments:scope_remove(id: number, link_id: number, callback?: function(entry|false, err?: string))`\
	Removes one scope link by `link_id`. Refuses to remove the last link (`"must keep at least one scope"`).\
	Broadcasts `database.punishments:scope_removed`.

- `#!ts punishments:sort(cache: table)`\
	Sort helper for cache ordering (permanent entries first, then longest expiry).

- `#!ts punishments:invalidate(identifier: Player|string)`\
	Clears active cache for identifier.

- `#!ts punishments:get(identifier: Player|string): table|false`\
	Returns cached active punishments for identifier.

- `#!ts punishments:designated(identifier: Player|string, type: string): table|false`\
	Returns first cached punishment matching `type`.

- `#!ts punishments:lookup(identifier: string, callback?: function(entries|false, err?: string))`\
	Cached read-through for active punishments (`duration` refresh window defaults to 1 hour).

## Runtime Events

- `#!ts punishments.invalidated(identifier?: string)`\
	Fired when the active punishment cache is cleared.\
	`identifier` is the player's SteamID64, or `nil` when the entire cache is flushed.

- `#!ts punishments.applied(invoker: Player, entries: table)`\
	Fired on `PlayerInitialSpawn` after a player's active punishments have been loaded from cache and are ready for enforcement.

- `#!ts punishments.added(entry: table)`\
	Fired after a punishment is inserted into the database and appended to the local active cache.

- `#!ts punishments.removed(entry: table)`\
	Fired after a punishment is hard-deleted from the database.

- `#!ts punishments.revoked(entry: table)`\
	Fired after a punishment's `revoker_id` is set and its active cache entry is removed.

- `#!ts punishments.updated(entry: table)`\
	Fired after a punishment field is mutated in-place (reason or duration updated via `rereason`/`reduration`).

- `#!ts punishments.expired(entry: table)`\
	Fired during the periodic expiration check when a cached entry's `expires_at` has passed.

## Hooks
GMod hooks fired alongside the dispatcher events above.\
Dispatchers are always first-order and used internally by BSA.

- `#!ts BSA.Punishments:added(entry: table)`\
	Fired after a punishment is inserted and cached.\
	Fires on both the issuing server and interlink receivers within scope.

- `#!ts BSA.Punishments:revoked(entry: table)`\
	Fired after a punishment is revoked and the active cache entry is removed.

- `#!ts BSA.Punishments:removed(entry: table)`\
	Fired after a punishment is hard-deleted.

- `#!ts BSA.Punishments:expired(entry: table)`\
	Fired during the periodic expiration check when an active entry's `expires_at` has passed.

- `#!ts BSA.Punishments:applied(invoker: Player, entries: table)`\
	Fired on `PlayerInitialSpawn` after the player's active punishments are loaded from cache.

## Notes
- `punishments.cache` is keyed by `player_identifier`, with read-through refresh via `lookup(...)` and hourly cache TTL metadata (`retrieve`, `duration`).
- Mutations (`add`, `revoke`, `remove`, `rereason`, `reduration`) update local cache and then broadcast through interlink channels under `database.punishments:*`.
- Receivers apply the same cache updates via `interlink:receive(...)` handlers (`add`, `revoke`, `remove`, `update`) and enforce provider/service/server scope checks before accepting payloads.
- On `interlink.changed`, cache is invalidated and online players are rehydrated from `active(...)`, maintaining cross-server cache coherence.

## Searcher Object
`punishments.searcher` is a query-builder class for punishment listings and totals.

### Builder Methods
- `#!ts punishments.searcher:active(state: boolean): self`
- `#!ts punishments.searcher:id(id: number): self`
- `#!ts punishments.searcher:type(type_name: string): self`
- `#!ts punishments.searcher:player(identifier_or_player_id: string|number): self`
- `#!ts punishments.searcher:invoker(identifier_or_player_id: string|number): self`
- `#!ts punishments.searcher:revoker(identifier_or_player_id: string|number): self`
- `#!ts punishments.searcher:reason(fragment: string): self`
- `#!ts punishments.searcher:hidden(include: boolean): self`\
	A one-directional filter: a falsy value excludes hidden rows (`hidden = 0`); a truthy value adds no clause (returns all, including hidden).
- `#!ts punishments.searcher:server(name_or_id: string|number): self`
- `#!ts punishments.searcher:service(name_or_id: string|number): self`
- `#!ts punishments.searcher:provider(name_or_id: string|number): self`
- `#!ts punishments.searcher:scope(server_id?: number, service_id?: number, provider_id?: number): self`
- `#!ts punishments.searcher:sort_by_created()`
- `#!ts punishments.searcher:sort_by_username()`
- `#!ts punishments.searcher:sort_by_expires()`
- `#!ts punishments.searcher:desc()`
- `#!ts punishments.searcher:asc()`
- `#!ts punishments.searcher:page(limit: number, offset?: number): self`
- `#!ts punishments.searcher:query(callback: function(rows|false))`\
Executes query and returns rows with `rows.statistics.count`.

## References

- [Variables - Punishments](variables/punishments.md): Shared realm, networked information and punishment functions.