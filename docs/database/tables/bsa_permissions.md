# bsa_permissions
Permissions define named capabilities that can be granted to groups.

!!! warning
    This table may incur high reads to the database due to its relevance!\
    Please ensure your platform follows the design requirements cache coherence.

## Structure
```sql
CREATE TABLE `bsa_permissions` (
    `perm_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `alias` TEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
```

- perm_id - unique id of the permission.
- name - unique permission name.
- alias - friendly display name.
- created_at - timestamp for when the permission was created.

## Design Requirements
- Treat `name` as immutable contract key across all platforms.
- Cache permission catalogs locally to avoid frequent full-table reads.
- On permission create/update/delete, propagate cache invalidation via command signaling.

## Interlink Behavior
- `database.permissions:add(permission)`
- `database.permissions:remove(permission)`
- `database.permissions:rename(permission, old_name, new_name)`
- `database.permissions:realias(permission, old_alias, new_alias)`
- Special case: ignore commands older than local permission `sync_time`.
