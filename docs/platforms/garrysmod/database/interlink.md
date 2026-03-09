# Interlink
Cross-server coordination layer for BSA database services.
Manages provider/service/server identity, command fanout (`bsa_command*` tables), acknowledgement polling, and server heartbeat state.

## Variables
- `#!ts interlink.poll_rate = 5`\
Polling interval (seconds) for incoming command checks.

- `#!ts interlink.heartbeat_rate = 30`\
Heartbeat interval (seconds) for `bsa_servers` presence updates.

- `#!ts interlink.outdated_constant = 3600`\
Command staleness constant (1 hour) used to align with DB automation expectations.

## Functions
- `#!ts interlink:alive(): boolean`\
Returns `true` when provider/service/server metadata is ready and global DB connection is alive.

- `#!ts interlink:receive(cmd: string, callback: function(server: table, ...: any))`\
Registers handler callback for an interlink command name.

- `#!ts interlink:broadcast(cmd: string, ...: any)`\
Broadcasts a command to all other servers through `sp_cmd_broadcast`.

- `#!ts interlink:send(specific: string|string[], cmd: string, ...: any)`\
Sends command only to named server(s) through `sp_cmd_send_names`.

- `#!ts interlink:omit(specific: string|string[], cmd: string, ...: any)`\
Sends command to all servers except named server(s) through `sp_cmd_omit_names`.

- `#!ts interlink:servers(search?: string, callback?: function(rows|false, err?: string))`\
Lists servers (joined with service name). Search matches server name/address.

- `#!ts interlink:providers(search?: string, callback?: function(rows|false, err?: string))`\
Lists providers; search matches provider `name`/`alias`.

- `#!ts interlink:services(search?: string, callback?: function(rows|false, err?: string))`\
Lists services; search matches service `name`/`alias`.

- `#!ts interlink:all(callback?: function(providers|false, services?: table, servers?: table, err?: string))`\
Fetches providers, services, and servers in one transaction.

- `#!ts interlink:poll(invalidate?: boolean, callback?: function(commands|false, err?: string))`\
Pulls pending commands expected for this server, inserts ACK rows, and executes registered handlers unless `invalidate` is `true`.

- `#!ts interlink:heartbeat(callback?: function(server|false, err?: string))`\
Upserts this server row in `bsa_servers`, updates heartbeat timestamp, and updates `interlink.server`.

## Runtime Events
- `#!ts interlink.connected(service, provider)`\
Invoked after provider/service discovery and first heartbeat.

- `#!ts interlink.disconnected()`\
Invoked when global DB connection drops.

- `#!ts interlink.changed(old_server, new_server)`\
Invoked when heartbeat resolves to a different `server_id` than before.

## Searcher Object
`interlink.searcher` is a query-builder class for server listing pages.

### Builder Methods
- `#!ts interlink.searcher:server(name_or_id: string|number): self`
- `#!ts interlink.searcher:service(name_or_id: string|number): self`
- `#!ts interlink.searcher:sort_by_name()`
- `#!ts interlink.searcher:sort_by_created()`
- `#!ts interlink.searcher:sort_by_heartbeat()`
- `#!ts interlink.searcher:desc()`
- `#!ts interlink.searcher:asc()`
- `#!ts interlink.searcher:page(limit: number, offset?: number): self`
- `#!ts interlink.searcher:query(callback: function(data|false))`\
Returns `{ statistics, servers, services, providers }` on success.

## Notes
- Command payloads are serialized/deserialized via `util.TableToJSON` and `util.JSONToTable`.
- During `poll`, handlers receive a shallow server object that includes `initiated_at` (converted from DB timezone to server timezone).
- `poll` is re-entry guarded by `interlink.polling` to prevent overlapping command consumption.