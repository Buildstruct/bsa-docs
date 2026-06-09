# bsa_punishments
Records punishments applied to players, with optional scope and expiration.

!!! danger
    This table may incur high reads to the database due to its relevance!\
    This table is notorious for being spammed by connections to servers.\
    Please ensure your platform follows the design requirements cache coherence.

## Structure
```sql
CREATE TABLE `bsa_punishments` (
    `punishment_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `player_id` BIGINT UNSIGNED NOT NULL,
    `invoker_id` BIGINT UNSIGNED NOT NULL,
    `revoker_id` BIGINT UNSIGNED NULL,
    `type` VARCHAR(64) NOT NULL,
    `reason` TEXT NOT NULL,
    `duration` BIGINT UNSIGNED NULL,
    `expires_at` DATETIME(6) GENERATED ALWAYS AS (
        CASE
            WHEN duration IS NULL THEN NULL
            ELSE DATE_ADD(created_at, INTERVAL duration SECOND)
        END
    ) STORED,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_pun_player
        FOREIGN KEY (`player_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_pun_invoker
        FOREIGN KEY (`invoker_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_pun_revoker
        FOREIGN KEY (`revoker_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE,

    INDEX idx_active_punishments (`player_id`, `expires_at`)
);
```

- punishment_id - unique id of the punishment.
- player_id - player being punished.
- invoker_id - player who created the punishment.
- revoker_id - player who revoked the punishment, if any.
- type - punishment type (`ban`, `warn`, `mute`, etc).
- reason - reason for the punishment.
- duration - duration in seconds; null means permanent.
- expires_at - computed expiration timestamp for timed punishments.
- created_at - timestamp for when the punishment was created.

!!! info
    Scope (provider/service/server) is stored in [bsa_punishment_links](bsa_punishment_links.md), not on this table.\
    A punishment applies to a platform only if it has at least one link covering that platform's identity.

## Notes
The `idx_active_punishments` index supports fast lookup of active punishments by player.

## Design Requirements
- Cache active punishments in memory per platform with short refresh windows.
- Query active punishments using `expires_at IS NULL OR expires_at > NOW(6)`.
- Treat `expires_at` as computed output; write only `duration` and `created_at` inputs.
- Scope coverage is determined by `bsa_punishment_links`; use `EXISTS` subqueries against that table when filtering by scope.
- Broadcast invalidation commands after punishment create/update/revoke events.

## Interlink Behavior
- `database.punishments:add(punishment, links)`
- `database.punishments:revoke(punishment)`
- `database.punishments:remove(punishment)`
- `database.punishments:update(punishment)`
