# bsa_command_routines
Stored procedures for writing command rows and target expectations.\
These procedures are the canonical write path for command fanout.

## Procedures

### sp_cmd_send_ids
Sends a command to a specific set of server IDs.

```sql
CREATE PROCEDURE sp_cmd_send_ids(
    IN p_origin_server_id BIGINT UNSIGNED,
    IN p_command TINYTEXT,
    IN p_argument JSON,
    IN p_targets_json JSON
)
```

- `p_origin_server_id` - sender server id.
- `p_command` - command name.
- `p_argument` - JSON payload.
- `p_targets_json` - JSON array of numeric server ids.

Behavior:

- Inserts one row into `bsa_command`.
- Inserts expected ACK rows in `bsa_command_expected` for alive targets only.
- Excludes the origin server.
- Returns `command_id`.

### sp_cmd_send_names
Sends a command to a specific set of server names.

```sql
CREATE PROCEDURE sp_cmd_send_names(
    IN p_origin_server_id BIGINT UNSIGNED,
    IN p_command TINYTEXT,
    IN p_argument JSON,
    IN p_target_names_json JSON
)
```

- `p_target_names_json` must be a JSON array of server names.

Behavior matches `sp_cmd_send_ids`, but resolves targets by `bsa_servers.name`.

### sp_cmd_broadcast
Sends a command to all alive servers except origin.

```sql
CREATE PROCEDURE sp_cmd_broadcast(
    IN p_origin_server_id BIGINT UNSIGNED,
    IN p_command TINYTEXT,
    IN p_argument JSON
)
```

Behavior:

- Inserts one row into `bsa_command`.
- Inserts expected ACK rows for every alive non-origin server.
- Returns `command_id`.

### sp_cmd_omit_ids
Broadcasts to alive servers except origin and omitted server IDs.

```sql
CREATE PROCEDURE sp_cmd_omit_ids(
    IN p_origin_server_id BIGINT UNSIGNED,
    IN p_command TINYTEXT,
    IN p_argument JSON,
    IN p_omit_json JSON
)
```

- `p_omit_json` must be a JSON array of numeric server ids.

### sp_cmd_omit_names
Broadcasts to alive servers except origin and omitted server names.

```sql
CREATE PROCEDURE sp_cmd_omit_names(
    IN p_origin_server_id BIGINT UNSIGNED,
    IN p_command TINYTEXT,
    IN p_argument JSON,
    IN p_omit_names_json JSON
)
```

- `p_omit_names_json` must be a JSON array of server names.

## Alive Server Rule
All fanout procedures currently define alive as:

```sql
s.heartbeat_at >= NOW() - INTERVAL 60 SECOND
```

## Design Requirements
- Use these procedures instead of direct inserts to `bsa_command_expected`.
- Pass valid JSON arrays; invalid shapes can result in empty target sets.
- Expect idempotent target writes via `INSERT IGNORE` in procedure internals.
- Keep server heartbeats current, otherwise targets are silently excluded.
- Acknowledge commands in `bsa_command_acknowledge` after successful local apply.
