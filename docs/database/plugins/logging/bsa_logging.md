# bsa_logging
Stores structured log entries emitted by game servers, bulk-uploaded from per-session flat files on server startup.

!!! info
    Log entries are not written to the database in real time.\
    Each server maintains a flat file during its runtime.\
    On next boot (or on manual rotation), the session file is bulk-uploaded into this table.

!!! warning
    This table can grow very large in active deployments.\
    Implement your own periodic stale-row cleanup policy using the `created_at` column.

## Structure
```sql
CREATE TABLE `bsa_logging` (
    `log_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `server_id` BIGINT UNSIGNED NOT NULL,
    `record` VARCHAR(255) NOT NULL,
    `entry` JSON NOT NULL,
    `uuid` VARCHAR(64) NOT NULL DEFAULT '',
    `seq` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL,

    INDEX `idx_logging_server_created` (`server_id`, `created_at` DESC),
    INDEX `idx_logging_record` (`record`),
    UNIQUE KEY `uk_logging_session` (`server_id`, `uuid`, `seq`),

    CONSTRAINT `fk_logging_server`
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- log_id - unique id of the log entry.
- server_id - server that produced this log entry.
- record - category/type of the log (e.g. `commands`, `spawns`).
- entry - JSON array describing the log content.
- uuid - session UUID generated at server startup; used with `seq` for idempotent backfill.
- seq - monotonic sequence number within the server's runtime session.
- created_at - timestamp set by the server at the time of the event, not the database insert time.

## Notes
The `uk_logging_session` unique key on `(server_id, uuid, seq)` prevents duplicate rows if the same session file is re-uploaded.\
This makes the bulk-upload operation safely idempotent.

The `idx_logging_server_created` index supports paginated queries ordered by server and time.\
The `idx_logging_record` index supports filtering by log category.

Searchable context such as invoker names and identifiers is stored in `bsa_logging_meta`, not in `entry` directly.\
Full-text search is performed via a joined subquery on the meta table.

## Design Requirements
- Set `created_at` to the event time from the server, not the database insertion time.
- Generate a fresh `uuid` per server runtime session at startup; never reuse a UUID across reboots.
- Increment `seq` monotonically within a session, do not reset until a new session UUID is generated.
- Upload session data idempotently, rely on `uk_logging_session` to safely skip duplicate rows on retry.
- Pair every inserted row with its metadata in `bsa_logging_meta` in the same bulk operation.
- Implement your own periodic cleanup that removes rows where `created_at` is older than a configurable retention window.
