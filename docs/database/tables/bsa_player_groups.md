# bsa_player_groups
Link table for additional group memberships for players.

## Structure
```sql
CREATE TABLE bsa_player_groups (
    `player_id` BIGINT UNSIGNED NOT NULL,
    `group_id`  BIGINT UNSIGNED NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    PRIMARY KEY (`player_id`, `group_id`),

    CONSTRAINT fk_pg_player
        FOREIGN KEY (`player_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_pg_group
        FOREIGN KEY (`group_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- player_id - player associated with the membership.
- group_id - group associated with the membership.
- created_at - timestamp for when this membership was created.

## Restrictions
Reserved groups cannot be linked without explicit SQL-session bypass.

- Group #1 (`system`) and group #2 (`console`) are blocked by triggers.
- Bypass exists only when session variable `@bsa_allow_reserved_group_assignment = 1`.

## Design Requirements
- Use `INSERT IGNORE` for idempotent grant operations.
- Remove only specific memberships instead of replacing full sets in concurrent systems.
- Recompute cached effective groups/permissions after membership changes.

## Interlink Behavior
- Secondary memberships are replicated through player commands (no `bsa_player_groups:*` channel).
- `database.players:secondaryadded(account, group, secondaries)`
- `database.players:secondaryremoved(account, group, secondaries)`
