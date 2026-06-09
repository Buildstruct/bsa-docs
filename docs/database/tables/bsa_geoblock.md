# bsa_geoblock
Stores connection block rules matched against IP, ISP, AS, or organization, with optional scope and revocation support.

## Structure

```sql
CREATE TABLE IF NOT EXISTS `bsa_geoblock` (
    `geoblock_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `invoker_id` BIGINT UNSIGNED NOT NULL,
    `revoker_id` BIGINT UNSIGNED NULL,
    `type` TINYTEXT NOT NULL,
    `match` TEXT NOT NULL,
    `reason` TEXT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_geoblock_invoker
        FOREIGN KEY (`invoker_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_geoblock_revoker
        FOREIGN KEY (`revoker_id`) REFERENCES `bsa_players`(`player_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

- geoblock_id - unique block rule identifier.
- invoker_id - player who created the block.
- revoker_id - player who revoked the block, `NULL` while active.
- type - match category: `ip`, `isp`, `as`, or `org`.
- match - value to match against, IP type supports CIDR notation (e.g. `10.0.0.0/24`).
- reason - reason for the block.
- created_at - creation timestamp.

!!! info
    Scope (provider/service/server) is stored in [bsa_geoblock_links](bsa_geoblock_links.md), not on this table.\
    A block rule enforces on a platform only if it has at least one link covering that platform's identity.

## Notes
`revoker_id` uses `ON DELETE SET NULL` so block history is preserved when the revoker's player row is removed.

## Design Requirements
- Active blocks are those where `revoker_id IS NULL`; platforms must cache only active, in-scope blocks.
- Scope coverage is determined via `EXISTS (SELECT 1 FROM bsa_geoblock_links WHERE ...)` against the platform's provider/service/server.
- Platforms must reload the active block cache on interlink connect and interlink scope change.
- Country and city must not be stored, only ISP, AS, org, and IP to avoid logging identifiable location data.

## Interlink Behavior
- `database.geoblock:add(entry, links)`
- `database.geoblock:revoke(entry)`
- `database.geoblock:remove(entry)`
- `database.geoblock:update(entry)`