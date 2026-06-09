# bsa_geoblock_links
Maps geoblock rules to one or more provider/service/server scopes.

## Structure

```sql
CREATE TABLE `bsa_geoblock_links` (
    `link_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `geoblock_id` BIGINT UNSIGNED NOT NULL,
    `service_id` BIGINT UNSIGNED NULL,
    `provider_id` BIGINT UNSIGNED NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT uq_geoblocklink_scope UNIQUE (`geoblock_id`, `service_id`, `provider_id`, `server_id`),

    CONSTRAINT fk_geoblocklink_geoblock
        FOREIGN KEY (`geoblock_id`) REFERENCES `bsa_geoblock`(`geoblock_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_geoblocklink_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_geoblocklink_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_geoblocklink_servers
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE ON UPDATE CASCADE
);
```

- link_id - unique link identifier.
- geoblock_id - geoblock rule this scope applies to.
- service_id - service scope; null = all services.
- provider_id - provider scope; null = all providers.
- server_id - server scope; null = all servers.
- created_at - timestamp for when the link was created.

## Notes
The unique constraint on `(geoblock_id, service_id, provider_id, server_id)` prevents duplicate scope entries per rule.

## Design Requirements
- A geoblock rule enforces on a platform only if at least one link covers that platform's provider/service/server.
- Active-block cache must be loaded using `EXISTS (SELECT 1 FROM bsa_geoblock_links WHERE ...)` against the platform's scope.
- All links are fetched as a JSON aggregate (`entry.links`) and passed verbatim on interlink broadcast.
- Receivers iterate `entry.links` to determine scope relevance before caching.
