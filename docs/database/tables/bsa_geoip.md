# bsa_geoip
Caches external geolocation lookups for IP addresses, storing ISP, AS, and organization data.

!!! info
    Entries are refreshed when older than one month.\
    No FK to `bsa_accounts` — the cache is independent of account lifecycle.

## Structure

```sql
CREATE TABLE IF NOT EXISTS `bsa_geoip` (
    `geoip_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `address` VARCHAR(46) NOT NULL UNIQUE,
    `isp` TEXT NOT NULL,
    `as` TEXT NOT NULL,
    `org` TEXT NOT NULL,
    `occurrence` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

- geoip_id - unique row identifier.
- address - IPv4 or IPv6 address (up to 46 chars), unique per row.
- isp - internet service provider name.
- as - autonomous system number and name string.
- org - organization name.
- occurrence - first time this address was resolved.
- updated - last time this entry was refreshed; used to determine cache freshness.

## Design Requirements
- Query with `updated >= NOW() - INTERVAL 1 MONTH` to respect the cache TTL.
- Upsert using `ON DUPLICATE KEY UPDATE` rather than separate insert/update paths.
- Private address ranges must not be inserted; check before lookup.