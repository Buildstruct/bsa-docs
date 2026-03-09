# Punishments
Read/write interface for `bsa_punishments` with scoped replication, active-cache management, and periodic expiration invalidation.

## Functions
- `#!ts punishments:add(target: Player|string, invoker: Player|string, type: string, duration?: number, reason: string, callback?: function(entry|false, err?: string))`\
Creates a punishment in current provider/service/server scope.

- `#!ts punishments:addex(target: Player|string, invoker: Player|string, type: string, duration?: number, reason: string, scope: {provider: boolean, service: boolean, server: boolean}, callback?: function(entry|false, err?: string))`\
Creates punishment with explicit scope flags.

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
- `#!ts punishments.invalidated(identifier?)`
- `#!ts punishments.applied(invoker: Player, entries)`
- `#!ts punishments.added(entry)`
- `#!ts punishments.removed(entry)`
- `#!ts punishments.revoked(entry)`
- `#!ts punishments.updated(entry)`
- `#!ts punishments.expired(entry)`

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
- `#!ts punishments.searcher:server(name_or_id: string|number): self`
- `#!ts punishments.searcher:service(name_or_id: string|number): self`
- `#!ts punishments.searcher:provider(name_or_id: string|number): self`
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