# bsa_groups
Groups define permission tiers and metadata used across services and providers.

!!! warning
    This table may incur high reads to the database due to its relevance!\
    Please ensure your platform follows the design requirements cache coherence.

## Structure
```sql
CREATE TABLE `bsa_groups` (
    `group_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `alias` TEXT NULL,
    `color` INT UNSIGNED NULL,
    `weight` INT UNSIGNED NOT NULL DEFAULT 0,
    `service_id` BIGINT UNSIGNED NULL,
    `provider_id` BIGINT UNSIGNED NULL,
    `server_id` BIGINT UNSIGNED NULL,
    `inherit_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_group_parent
        FOREIGN KEY (`inherit_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE,

    CONSTRAINT fk_group_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_group_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_group_servers
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    INDEX idx_weight (weight)
);
```

- group_id - unique id of the group.
- name - unique group name, such as `administrator`.
- alias - friendly display name.
- color - optional display color; null means resolved via fallback/inheritance.
- weight - hierarchy and priority value.
- service_id - service scope; null means all services.
- provider_id - provider scope; null means all providers.
- server_id - server scope; null means all servers.
- inherit_id - parent group to inherit permissions/metadata from.
- created_at - timestamp for when the group was created.

## Restrictions
Core groups are protected by triggers.

- 1 - `system`
- 2 - `console`
- 3 - `user`

Core groups cannot be deleted.
Core group IDs cannot be changed.

## Design Requirements
- Resolve effective permissions by inheritance chain plus direct grants.
- Prevent inheritance loops in application logic before writes.
- Prefer immutable `name` values as cross-platform identifiers.
- Cache group catalogs locally to avoid frequent full-table reads.
- On group create/update/delete, propagate cache invalidation via command signaling.
