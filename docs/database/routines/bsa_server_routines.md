# bsa_server_cleanup
Cleanup automation for temporary server lifecycle.

## Event

### ev_cleanup_servers
Runs every minute.

```sql
CREATE EVENT IF NOT EXISTS ev_cleanup_servers
    ON SCHEDULE EVERY 1 MINUTE
    DO
    DELETE FROM bsa_servers
    WHERE temporary = 1
      AND heartbeat_at < NOW() - INTERVAL 60 SECOND;
```

Behavior:

- Deletes servers marked as `temporary` whose heartbeat has exceeded 60 seconds.

## Procedure

### sp_cleanup_servers
Manual cleanup entry point with the same logic as the event.

```sql
CREATE PROCEDURE IF NOT EXISTS sp_cleanup_servers()
```

Use this when event scheduler is disabled or when forcing immediate cleanup.

## Design Requirements
- Enable MySQL event scheduler in deployments that rely on automatic cleanup.
- If events are disabled, run `CALL sp_cleanup_servers();` on a fixed schedule.
- Do not repurpose or recycle temporary server rows; delete and re-register on reconnect.
- Keep cleanup cadence aligned with the 60-second staleness threshold defined in `bsa_servers`.
- Temporary servers must never be treated as permanent; do not clear the `temporary` flag to retain a row.
