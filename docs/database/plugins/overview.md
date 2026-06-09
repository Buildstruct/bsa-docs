# Plugins
These are database additions that allows for extensions to all platforms for potential usage.

!!! abstract
	We designed the database so that you can always choose to expand it as much as you need.\
	As we understand that some communities may have certain stakeholders that do not compare to ours.

## Design Requirements
1. Plugins implemented through the database **MUST** reflect its functionality on all platforms when individually enabled.
       - Deviating from a plugin's design requirements may cause desyncing and data inaccuracies across platforms, resulting in corruption of information.

2. Plugins also do not need to be enabled across all servers, since not all servers may support them or could be platform specific.

3. Foreign keys must include cascading constraints on UPDATE and DELETE to maintain data assocations.

## Columns vs Foreign
In the database you may have noticed info boxes on "column additions" and "foreign key".\
There is a clear difference to these depending on your requirements.

As an example, let's look at [bsa_players](../tables/bsa_players.md) and add some new data to it.

If data can be tied to each player, and only one of it should exist per-player, then we can just add a column like so, which is a 1:1 relation:
```sql
ALTER TABLE `bsa_players`
    ADD COLUMN `resource_id` BIGINT UNSIGNED NOT NULL DEFAULT 0;
```

But if multiple data must be stored on each player, then we should ideally create a new table and foriegn key the `player_id`, which is a 1:N relation:
```sql
CREATE TABLE `plugin_player_kills` (
    `kill_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `player_id` BIGINT UNSIGNED NOT NULL,
    `victim_id` BIGINT UNSIGNED NOT NULL,
    `killed_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_kills_player
        FOREIGN KEY (`player_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_kills_victim
        FOREIGN KEY (`victim_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

Keep in mind for foriegn keys its important to use constraints to maintain data assocations.

## Joining Tables

A lot of times when you are developing with these you would want to combine data together.\
A rule of thumb for these is try to make it a single query if you can, this will reduce overhead of multiple queries from a single transaction.\
As an example we should look at `plugin_player_kills`, we want to maybe get the username of the `player_id` from `steam` providers from [bsa_accounts](../tables/bsa_accounts.md).

```sql
SELECT
    k.kill_id,
    k.player_id,
    ap.username AS player_username,
    k.victim_id,
    av.username AS victim_username,
    k.killed_at
FROM `plugin_player_kills` k
JOIN `bsa_providers` p ON p.name = 'steam'
JOIN `bsa_accounts` ap ON ap.player_id = k.player_id AND ap.provider_id = p.provider_id
JOIN `bsa_accounts` av ON av.player_id = k.victim_id AND av.provider_id = p.provider_id
```

Depending on your requirements, consider whether `JOIN` (inner), `LEFT JOIN`, or `RIGHT JOIN` is appropriate, outer joins will return `NULL` for columns where no match exists, which may be desirable if related data is optional.