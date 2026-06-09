# bsa_group_permissions
Links permissions to groups, optionally scoped by service, provider, or server.

## Structure
```sql
CREATE TABLE `bsa_group_permissions` (
    `link_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `group_id` BIGINT UNSIGNED NOT NULL,
    `perm_id`  BIGINT UNSIGNED NOT NULL,
    `service_id` BIGINT UNSIGNED NULL,
    `provider_id` BIGINT UNSIGNED NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT uq_group_perms UNIQUE (`group_id`, `perm_id`, `service_id`, `provider_id`, `server_id`),

    CONSTRAINT fk_permission_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_permission_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_permission_servers
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_permission_groups
        FOREIGN KEY (`group_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_group_permissions
        FOREIGN KEY (`perm_id`) REFERENCES `bsa_permissions`(`perm_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- link_id - unique id for the permission link.
- group_id - group that receives the permission.
- perm_id - permission granted to the group.
- service_id - service scope; null means all services.
- provider_id - provider scope; null means all providers.
- server_id - server scope; null means all servers.
- created_at - timestamp for when the link was created.

## Restrictions
The tuple (`group_id`, `perm_id`, `service_id`, `provider_id`, `server_id`) must be unique.

## Design Requirements
- Evaluate scoped grants from most specific to least specific.
- Use `NULL` as wildcard scope in permission resolution.
- Cache effective permission sets and invalidate via command signaling on writes.
- Use idempotent inserts (`INSERT IGNORE` or upsert patterns) in distributed writers.

## Interlink Behavior
- `database.groups.permissions:add(link, group, permission, is_new_for_group_cache)`
- `database.groups.permissions:remove(link, group, permission, fully_removed_from_group_cache)`
- Special case: apply `provider_id` / `service_id` / `server_id` gates on receive.
- Special case: ignore commands older than local permission-link `sync_time`.
