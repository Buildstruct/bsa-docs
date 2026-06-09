# bsa_players
Players are the base entities that own accounts and group memberships.

!!! warning
    This table may incur high reads to the database due to its relevance!\
    Please ensure your platform isn't requesting information so often.

!!! info
    This is an expandable table, you may add/remove columns here without issue.\
    Please keep `player_id`, `group_id`, `created_at` as is, these are required by BSA.\
    You may also foreign key this table as well if you don't plan on adding more columns.

## Structure
```sql
CREATE TABLE `bsa_players` (
    `player_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `group_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_players_group
        FOREIGN KEY (`group_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);
```

- player_id - unique id of the player.
- group_id - primary group for the player.
- created_at - timestamp for when the player was created.

## Restrictions
Core players are protected by triggers.

- 1 - `SYSTEM`
- 2 - `CONSOLE`

Core players cannot be updated or deleted.\
Reserved groups are protected by triggers.

- Group #1 (`system`) and group #2 (`console`) cannot be assigned to normal players.
- Bypass exists only when session variable `@bsa_allow_reserved_group_assignment = 1`.

## Design Requirements
- Create normal players without assigning reserved groups.
- Treat `group_id` as primary group only; additional groups belong in `bsa_player_groups`.
- Do not expose reserved-group bypass to runtime platform code.

## Interlink Behavior
- `database.players:connected(account, secondaries)`
- `database.players:disconnected(account, secondaries)`
- `database.players:timeset(account, time_seconds)`
- `database.players:primaryset(account, group, secondaries)`
- `database.players:secondaryadded(account, group, secondaries)`
- `database.players:secondaryremoved(account, group, secondaries)`
- Special case: player/account flows are provider-specific in current GMod handlers.
