# bsa_sessions
Sessions represent live or recently-live account presence on servers.\
An account may have multiple session rows at once.

!!! warning
    This table may incur high reads to the database due to online-state lookups.\
    Please ensure your platform isn't requesting information so often.

## Structure
```sql
CREATE TABLE `bsa_sessions` (
    `session_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `account_id` BIGINT UNSIGNED NOT NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `heartbeat_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_conn_server
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE,

    CONSTRAINT fk_conn_account
        FOREIGN KEY (`account_id`) REFERENCES `bsa_accounts`(`account_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- session_id - unique id of the session.
- account_id - account that owns this session.
- server_id - server currently attached to the session; null means detached or orphaned from a server record.
- heartbeat_at - timestamp for the last session heartbeat.
- created_at - timestamp for when the session row was created.

## Restrictions
- There are no trigger-protected rows in this table.
- Multiple sessions per account are allowed by design.
- Deleting an account cascades and deletes its sessions.
- Deleting a server does not delete sessions; it sets `server_id` to `NULL`.

## Design Requirements
- Treat a session as alive only when `heartbeat_at` is within 60 seconds, and the linked server heartbeat in `bsa_servers` is also within 60 seconds.
- Create a new row when a player/account attaches to a server and no reusable `session_id` is already held locally.
- Refresh `heartbeat_at` regularly for active sessions, the current platform also refreshes `server_id` on heartbeat.
- Delete the row on clean disconnect/shutdown rather than keeping indefinite session history.
- Always propagate `session_id` with replicated account presence so remote caches can update the correct live entry.

## Interlink Behavior
- `database.players:connected(account, secondaries)` payloads must include `session_id`.
- `database.players:disconnected(account, secondaries)` payloads must include `session_id`.
- On interlink reconnect/startup, platforms should clear any stale sessions owned by their current `server_id` and broadcast matching disconnect events.
