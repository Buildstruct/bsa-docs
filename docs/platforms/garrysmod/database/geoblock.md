# {{ realm("server") }} GeoBlock
Read/write interface for `bsa_geoblock` with in-scope active-block cache, interlink replication, and enforcement.

!!! info
    See [core/database/tables/geoblock.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/tables/geoblock.lua) for the actual design implementation.\
    See [bsa_geoblock](../../../database/tables/bsa_geoblock.md) for table structure & design requirements.

## Functions

- `#!ts geoblock:add(invoker: Player|string, type: string, match: string, reason: string, scopes: table, callback?: function(entry|false, err?: string))`\
  Inserts a new block rule.\
  `type` must be one of `"ip"`, `"isp"`, `"as"`, or `"org"`.\
  `match` for `"ip"` type accepts CIDR notation.\
  `scopes` is a list of `{provider_id: number?, service_id: number?, server_id: number?}` tables; each entry becomes one row in `bsa_geoblock_links`.

- `#!ts geoblock:revoke(id: number, revoker: Player|string, callback?: function(entry|false, err?: string))`\
  Sets `revoker_id` on the block row and removes the entry from the local cache.

- `#!ts geoblock:remove(id: number, callback?: function(entry|false, err?: string))`\
  Hard-deletes the block row and removes it from the local cache.

- `#!ts geoblock:rereason(id: number, new_reason: string, callback?: function(entry|false, err?: string))`\
  Updates the reason field in-place and patches the cached copy.

- `#!ts geoblock:exist(id: number, callback: function(entry|false, err?: string))`\
  Fetches a single block entry by `geoblock_id` from the database.

- `#!ts geoblock:refresh(callback?: function(cache|false))`\
  Reloads all active in-scope blocks from `bsa_geoblock` into `geoblock.cache`.

- `#!ts geoblock:match(geo: {ip: string, isp: string, as: string, org: string}): entry|false`\
  Scans `geoblock.cache` for a matching active block.\
  Returns the first match or `false`.

## Runtime Events

- `#!ts geoblock.added(entry: table)`\
  Fired when a block is inserted, locally or via interlink.

- `#!ts geoblock.removed(entry: table)`\
  Fired when a block is hard-deleted, locally or via interlink.

- `#!ts geoblock.revoked(entry: table)`\
  Fired when a block is revoked, locally or via interlink.

- `#!ts geoblock.updated(entry: table)`\
  Fired when a block's reason is changed, locally or via interlink.

## Notes
- `geoblock.cache` holds only active (`revoker_id IS NULL`), in-scope entries for the current server.
  - It is populated on interlink connect and on scope change.
- Mutations update the local cache then broadcast through interlink `database.geoblock:*` channels.
  - Receivers apply the same cache update after passing the scope gate.

## Searcher Object

`geoblock.searcher` is a query-builder class for block listings and totals.

### Builder Methods

- `#!ts geoblock.searcher:active(state: boolean): self`
- `#!ts geoblock.searcher:id(id: number): self`
- `#!ts geoblock.searcher:type(type_name: string): self`
- `#!ts geoblock.searcher:match(value: string): self`
- `#!ts geoblock.searcher:invoker(identifier_or_player_id: string|number): self`
- `#!ts geoblock.searcher:revoker(identifier_or_player_id: string|number): self`
- `#!ts geoblock.searcher:reason(fragment: string): self`
- `#!ts geoblock.searcher:server(name_or_id: string|number): self`
- `#!ts geoblock.searcher:service(name_or_id: string|number): self`
- `#!ts geoblock.searcher:provider(name_or_id: string|number): self`
- `#!ts geoblock.searcher:sort_by_created()`
- `#!ts geoblock.searcher:sort_by_type()`
- `#!ts geoblock.searcher:sort_by_match()`
- `#!ts geoblock.searcher:desc()`
- `#!ts geoblock.searcher:asc()`
- `#!ts geoblock.searcher:page(limit: number, offset?: number): self`
- `#!ts geoblock.searcher:query(callback: function(rows|false))`\
  Executes query and returns rows with `rows.statistics.count`.
