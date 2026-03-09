# bsa_command_cleanup
Cleanup automation for command queue lifecycle.

## Event

### ev_cleanup_commands
Runs every minute.

```sql
CREATE EVENT IF NOT EXISTS ev_cleanup_commands
    ON SCHEDULE EVERY 1 MINUTE
    DO
    BEGIN
        DELETE FROM bsa_command
        WHERE created_at < NOW() - INTERVAL 1 HOUR;

        DELETE c
        FROM bsa_command c
        WHERE NOT EXISTS (
            SELECT 1
            FROM bsa_command_expected e
            WHERE e.command_id = c.command_id
                AND NOT EXISTS (
                    SELECT 1
                    FROM bsa_command_acknowledge a
                    WHERE a.command_id = e.command_id
                      AND a.server_id  = e.server_id
            )
        );
    END
```

Behavior:

- Deletes stale commands older than 1 hour.
- Deletes commands fully acknowledged by all expected recipients.

## Procedure

### sp_cleanup_commands
Manual cleanup entry point with the same logic as the event.

```sql
CREATE PROCEDURE IF NOT EXISTS sp_cleanup_commands()
```

Use this when event scheduler is disabled or when forcing immediate cleanup.

## Design Requirements
- Enable MySQL event scheduler in deployments that rely on automatic cleanup.
- If events are disabled, run `CALL sp_cleanup_commands();` on a fixed schedule.
- Do not rely on `bsa_command` for long-term history; rows are intentionally short-lived.
- Keep cleanup cadence aligned with command polling cadence.
- Treat missing command rows as normal after successful processing/ACK convergence.
