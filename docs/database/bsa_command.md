# bsa_command
Commands used to broadcast critical actions to servers.\
This is a lightweight database-backed signaling channel, not a high-throughput message bus.

## Structure
```sql
CREATE TABLE `bsa_command` (
    `command_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `server_id` BIGINT UNSIGNED NOT NULL,
    `command` TINYTEXT NOT NULL,
    `argument` JSON NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_cmd_server
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- command_id - unique id of the command.
- server_id - server that created the command.
- command - command string.
- argument - JSON payload for the command.
- created_at - timestamp for when the command was created.

## Design Requirements
- Prefer stored procedures (`sp_cmd_send_ids`, `sp_cmd_send_names`, `sp_cmd_broadcast`, `sp_cmd_omit_ids`, `sp_cmd_omit_names`) to build command fanout safely.
- Acknowledge received commands using `bsa_command_acknowledge` after successful processing.
- Poll in short intervals and process in ascending `command_id` to preserve expected ordering.
- Keep payloads compact; large payloads should be fetched by ID from dedicated tables.
- Treat this table as signaling only, not durable audit/event storage.

## Common Command Flow

### Sender inserts command and fanout targets
Use one of the send procedures (example: broadcast).

```sql
CALL sp_cmd_broadcast(
    ?,
    'permissions.invalidate',
    JSON_OBJECT('scope', 'all')
);
```

### Receiver polls pending commands
Poll commands expected for this server that are not yet acknowledged.

```sql
SELECT c.command_id, c.command, c.argument, c.created_at
FROM bsa_command c
JOIN bsa_command_expected e
    ON e.command_id = c.command_id
LEFT JOIN bsa_command_acknowledge a
    ON a.command_id = c.command_id
   AND a.server_id = e.server_id
WHERE e.server_id = ?
  AND a.command_id IS NULL
ORDER BY c.command_id ASC;
```

### Receiver applies command logic
Apply command idempotently in platform code.

### Receiver writes ACK
Write ACK only after successful local apply.

```sql
INSERT IGNORE INTO bsa_command_acknowledge(command_id, server_id)
VALUES (?, ?);
```

### Cleanup removes completed/stale rows
- Automatic: `ev_cleanup_commands` runs every minute.
- Manual: `CALL sp_cleanup_commands();`
