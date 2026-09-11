# bsa_server_metadata
Free-form key/value metadata reported by a server alongside its heartbeat.

## Structure
```sql
CREATE TABLE `bsa_server_metadata` (
    `server_id` BIGINT UNSIGNED NOT NULL,
    `meta_key` VARCHAR(64) NOT NULL,
    `meta_value` TEXT NULL,
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),

    PRIMARY KEY (`server_id`, `meta_key`),

    CONSTRAINT fk_servermeta_server
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- server_id - server the metadata belongs to.
- meta_key - platform-defined key, such as `map` or `gamemode`.
- meta_value - platform-defined value, stored as text.
- updated_at - timestamp for when the row was last written.

## Restrictions
- The tuple (`server_id`, `meta_key`) must be unique.
- Keys are free-form. BSA reserves no keys and enforces no schema on the values.
- Rows are removed automatically when the owning `bsa_servers` row is deleted.

## Design Requirements
- Platforms replace the full key set for their own `server_id` on each heartbeat. Keys not sent in a beat are deleted.
- Only manage metadata for your own `server_id`, never write rows on behalf of another server.
- Values are transmitted as text, convert numbers and booleans before writing.
- Treat metadata as untrusted display data; do not use it for authorization or scope decisions.
- Hidden servers must not expose metadata through a public surface. Apply the same visibility rule as the server row itself.

## Related
- [bsa_servers](bsa_servers.md) owns each metadata row.
- [bsa_interlink](../bsa_interlink.md) defines when platforms write metadata.
