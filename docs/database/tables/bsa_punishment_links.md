# bsa_punishment_links
Maps punishments to one or more provider/service/server scopes.

## Structure

```sql
CREATE TABLE `bsa_punishment_links` (
    `link_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `punishment_id` BIGINT UNSIGNED NOT NULL,
    `service_id` BIGINT UNSIGNED NULL,
    `provider_id` BIGINT UNSIGNED NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT uq_punlink_scope UNIQUE (`punishment_id`, `service_id`, `provider_id`, `server_id`),

    CONSTRAINT fk_punlink_punishment
        FOREIGN KEY (`punishment_id`) REFERENCES `bsa_punishments`(`punishment_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_punlink_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_punlink_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_punlink_servers
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE ON UPDATE CASCADE
);
```

- link_id - unique link identifier.
- punishment_id - punishment this scope applies to.
- service_id - service scope; null = all services.
- provider_id - provider scope; null = all providers.
- server_id - server scope; null = all servers.
- created_at - timestamp for when the link was created.

## Notes
The unique constraint on `(punishment_id, service_id, provider_id, server_id)` prevents duplicate scope entries per punishment.

## Design Requirements
- A punishment applies on a platform only if at least one link covers that platform's provider/service/server.
- Scope filtering must use `EXISTS (SELECT 1 FROM bsa_punishment_links WHERE ...)` rather than columns on `bsa_punishments`.
- All links are fetched as a JSON aggregate (`entry.links`) alongside the punishment row and passed verbatim on interlink broadcast.
- Receivers iterate `entry.links` to determine scope relevance before caching.
