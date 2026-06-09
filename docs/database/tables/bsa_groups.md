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
    `inherit_id` BIGINT UNSIGNED NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_group_parent
        FOREIGN KEY (`inherit_id`) REFERENCES `bsa_groups`(`group_id`)
            ON DELETE SET NULL
            ON UPDATE CASCADE,

    INDEX idx_weight (weight)
);
```

- group_id - unique id of the group.
- name - unique group name, such as `administrator`.
- alias - friendly display name.
- color - optional display color; null means resolved via fallback/inheritance.
- weight - hierarchy and priority value.
- inherit_id - parent group to inherit permissions/metadata from.
- created_at - timestamp for when the group was created.

!!! info
    Scope (provider/service/server) is stored in [bsa_group_links](bsa_group_links.md), not on this table.\
    A group is visible to a platform only if it has at least one link covering that platform's identity.

## Restrictions
Core groups are protected by triggers.

- 1 - `system`
- 2 - `console`
- 3 - `user`

Core groups cannot be deleted.
Core group IDs cannot be changed.

## Design Requirements
- Load groups via JOIN on `bsa_group_links` filtered to the platform's provider/service/server scope.
- Cached group objects carry a `links` array of all scope links that covered the platform at sync time.
- `group.perms` holds permission grants covering this platform; `group.all_perms` holds grants across all scopes.
- Resolve effective permissions by inheritance chain plus direct grants.
- Prevent inheritance loops in application logic before writes.
- Prefer immutable `name` values as cross-platform identifiers.
- Cache group catalogs locally to avoid frequent full-table reads.
- On group create/update/delete, propagate cache invalidation via command signaling.
- Scope authority for an operation requires both a group link covering the target and a permission grant covering the target.

## Interlink Behavior
- `database.groups:add(group, link)`
- `database.groups:remove(group)`
- `database.groups:link(group, link)`
- `database.groups:unlink(group, link)`
- `database.groups:rescope(group, link)`
- `database.groups:scope_added(group, link)`
- `database.groups:scope_removed(group, link)`
- `database.groups:rename(group, old_name, new_name)`
- `database.groups:realias(group, old_alias, new_alias)`
- `database.groups:reweight(group, old_weight, new_weight)`
- `database.groups:recolor(group, old_color_u32, new_color_u32)`
- `database.groups:reinherit(group, old_inherit_id, new_inherit_id)`
- Special case: ignore commands older than local `sync_time`.
