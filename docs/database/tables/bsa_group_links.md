# bsa_group_links
Maps groups to one or more provider/service/server scopes.

## Structure

```sql
CREATE TABLE `bsa_group_links` (
    `link_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `group_id` BIGINT UNSIGNED NOT NULL,
    `service_id` BIGINT UNSIGNED NULL,
    `provider_id` BIGINT UNSIGNED NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT uq_grouplink_scope UNIQUE (`group_id`, `service_id`, `provider_id`, `server_id`),

    CONSTRAINT fk_grouplink_group
        FOREIGN KEY (`group_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_grouplink_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_grouplink_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_grouplink_servers
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE ON UPDATE CASCADE
);
```

- link_id - unique link identifier.
- group_id - group this scope applies to.
- service_id - service scope; null = all services.
- provider_id - provider scope; null = all providers.
- server_id - server scope; null = all servers.
- created_at - timestamp for when the link was created.

## Notes
The unique constraint on `(group_id, service_id, provider_id, server_id)` prevents duplicate scope entries per group.

## Design Requirements
- A group with no links is invisible to all platforms, core groups (1–3) ship with an initial wildcard link (`NULL, NULL, NULL`).
- Platforms load groups via JOIN on this table, filtered to matching scope — a group appears in cache only if at least one link covers that platform's provider/service/server.
- On interlink receive, commands gate on the accompanying link before applying cache updates.
- `entry.links` in cached group objects holds all links that covered the receiving platform at sync time.
