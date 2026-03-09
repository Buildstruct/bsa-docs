# Groups
Read/write interface for `bsa_groups` plus scoped group-permission links (`bsa_group_permissions`). Includes local cache synchronization and interlink replication handlers.

## Constants
- `#!ts BSA.Storage.Groups.SYSTEM = 1`
- `#!ts BSA.Storage.Groups.CONSOLE = 2`
- `#!ts BSA.Storage.Groups.USER = 3`

## Functions
- `#!ts groups:sync(callback?: function(ok: boolean, err?: string))`\
Refreshes group cache and group-permission cache for active provider/service/server scope.

- `#!ts groups:add(name: string, alias?: string, weight: number, scope: {provider: boolean, service: boolean, server: boolean}, inherit?: string|number, callback?: function(group|false, err?: string))`\
Creates a group. Optional inheritance resolves from existing group name.

- `#!ts groups:remove(name_id: string|number, callback?: function(group|false, err?: string))`\
Deletes by name or `group_id` in current scope.

- `#!ts groups:rename(name_id: string|number, new_name: string, callback?: function(group|false, err?: string))`\
Renames a group and updates cache keys.

- `#!ts groups:realias(name_id: string|number, new_alias?: string, callback?: function(group|false, err?: string))`\
Sets alias or clears alias (`NULL`).

- `#!ts groups:reweight(name_id: string|number, new_weight: number, callback?: function(group|false, err?: string))`\
Updates group weight.

- `#!ts groups:rescope(name_id: string|number, scope: {provider: boolean, service: boolean, server: boolean}, callback?: function(group|false, err?: string))`\
Rewrites scope columns (`provider_id`, `service_id`, `server_id`).

- `#!ts groups:recolor(name_id: string|number, new_color?: Color|number, callback?: function(group|false, err?: string))`\
Sets color (`u32`) or clears it.

- `#!ts groups:reinherit(name_id: string|number, new_inherit?: string|number, callback?: function(group|false, err?: string))`\
Changes `inherit_id` or clears inheritance.

- `#!ts groups:get(name_id?: string|number): table|nil`\
Returns full cache when omitted, otherwise a specific group.

- `#!ts groups:inheritances(name_id: string|number): table`\
Returns linear inheritance chain (guarded against circular loops; max depth 128).

## Runtime Events
- `#!ts groups.added(group)`
- `#!ts groups.removed(group)`
- `#!ts groups.renamed(group, old_name, new_name)`
- `#!ts groups.realiased(group, old_alias, new_alias)`
- `#!ts groups.reweighted(group, old_weight, new_weight)`
- `#!ts groups.recolored(group, old_color?: Color, new_color?: Color)`
- `#!ts groups.reinherited(group, old_inherit_id?: number, new_inherit_id?: number)`
- `#!ts groups.rescoped(group)`
- `#!ts groups.synced()`

## Group Permission Links (`groups.Permissions`)
Nested manager for `bsa_group_permissions` rows.

### Functions
- `#!ts groups.Permissions:sync(callback?: function(ok: boolean, err?: string))`\
Rebuilds permission-link cache and repopulates each group's `perms`/`iperms` lookup tables.

- `#!ts groups.Permissions:add(group_name: string|number, permission_name: string|number, callback?: function(link|false, group?, permission?, is_new?: boolean))`\
Adds scoped link using current interlink provider/service/server.

- `#!ts groups.Permissions:addex(group_name: string|number, permission_name: string|number, scope: {provider: boolean, service: boolean, server: boolean}, callback?: function(link|false, group?, permission?, is_new?: boolean))`\
Adds link with explicit scope flags.

- `#!ts groups.Permissions:remove(link_id: number, callback?: function(link|false, group?, permission?, deletion?: boolean))`\
Removes link by `link_id` and updates group permission lookup state.

### Runtime Events
- `#!ts groups.Permissions.added(link, group, permission, is_new)`
- `#!ts groups.Permissions.removed(link, group, permission, deletion)`
- `#!ts groups.Permissions.synced()`

## Notes
- Changes are broadcast with interlink channels under `database.groups:*` and reflected on receivers if event timestamps are newer than local `sync_time`.

## References

- [Variables - Groups](variables/groups.md): Shared realm and networked groups.