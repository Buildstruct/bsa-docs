# bsa_interlink
Interlink is the cross-server synchronization protocol built on top of `bsa_servers` and `bsa_command*`.\
It is used by platforms to keep local caches coherent and to forward state-change signals.\
While we could have used Websockets, RPC or MQ, we decided to use internal SQL queries to better support a wide variety of solutions with minimal dependency impact.

## Runtime Lifecycle
1. Platform starts and resolves provider/service identity (`bsa_providers`, `bsa_services`).
2. Platform heartbeats into `bsa_servers` (default every 30s).
3. Platform polls `bsa_command` fanout (default every 5s).
4. Platform ACKs seen commands in `bsa_command_acknowledge`.
5. Registered handlers update local cache/state and invoke local events.

See [bsa_commands](tables/bsa_command.md) for more information on the SQL requirements.

## Scope Contract
Most replicated entities use nullable scope fields:

- `provider_id = NULL` means all providers.
- `service_id = NULL` means all services.
- `server_id = NULL` means all servers.

Receivers should ignore commands that do not match their current scope.

## Sync-Time Contract
For hot caches, handlers compare:

- `server.initiated_at` (command creation time converted to server timezone)
- local `sync_time`

If command time is older than last full sync, command is skipped to avoid stale replay.

## Command Names In Use

### Groups
- `database.groups:add(group, link)`
- `database.groups:remove(group)`
- `database.groups:link(group, link)`
- `database.groups:unlink(group, link)`
- `database.groups:rescope(group, link)`
- `database.groups:scope_added(group, link)`
- `database.groups:scope_removed(group, link)`
- `database.groups:rename(group, old_name, new_name)`
- `database.groups:realias(group, old_alias, new_alias)`
- `database.groups:reweight(group, old_weight, new_weight)`
- `database.groups:recolor(group, old_color_u32, new_color_u32)`
- `database.groups:reinherit(group, old_inherit_id, new_inherit_id)`

### Group Permissions
- `database.groups.permissions:add(link, group, permission, is_new_for_group_cache)`
- `database.groups.permissions:remove(link, group, permission, fully_removed_from_group_cache)`

### Permissions
- `database.permissions:add(permission)`
- `database.permissions:remove(permission)`
- `database.permissions:rename(permission, old_name, new_name)`
- `database.permissions:realias(permission, old_alias, new_alias)`

### Players
- `database.players:connected(account, secondaries)`
- `database.players:disconnected(account, secondaries)`
- `database.players:timeset(account, time_seconds)`
- `database.players:primaryset(account, group, secondaries)`
- `database.players:secondaryadded(account, group, secondaries)`
- `database.players:secondaryremoved(account, group, secondaries)`

### Punishments
- `database.punishments:add(punishment, links)`
- `database.punishments:revoke(punishment)`
- `database.punishments:remove(punishment)`
- `database.punishments:update(punishment)`

### GeoBlock
- `database.geoblock:add(entry, links)`
- `database.geoblock:revoke(entry)`
- `database.geoblock:remove(entry)`
- `database.geoblock:update(entry)`

## Compatibility Notes
- New platforms should accept both names to remain compatible with existing deployments.
- If a cache entry is missing on receive, platform should fall back to full sync/reload.
