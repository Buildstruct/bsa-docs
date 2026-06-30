# {{ realm("server") }} Permissions
Read/write interface for global permission templates in `bsa_permissions`, with interlink replication and local cache updates.

!!! info
	See [core/database/tables/permissions.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/tables/permissions.lua) for the actual design implementation.\
	See [bsa_permissions](../../../database/tables/bsa_permissions.md) for implementation & design requirements.

## Functions
- `#!ts permissions:sync(callback?: function(ok: boolean, err?: string))`\
Reloads all permissions into cache (`perm_id` and `name` keys).

- `#!ts permissions:add(name: string, alias?: string, callback?: function(permission|false, err?: string))`\
Creates a permission if missing.\
A temporary in-memory guard prevents concurrent duplicate inserts for the same name.

- `#!ts permissions:remove(name_id: string|number, callback?: function(permission|false, err?: string))`\
Deletes by name or `perm_id`.

- `#!ts permissions:rename(name_id: string|number, new_name: string, callback?: function(permission|false, err?: string))`\
Renames permission and rewires cache keys.

- `#!ts permissions:realias(name_id: string|number, new_alias?: string, callback?: function(permission|false, err?: string))`\
Sets alias or clears alias (`NULL`).

- `#!ts permissions:get(name_id?: string|number): table|nil`\
Returns full cache when omitted, otherwise a single permission.

## Runtime Events
- `#!ts permissions.added(permission)`
- `#!ts permissions.removed(permission)`
- `#!ts permissions.renamed(permission, old_name, new_name)`
- `#!ts permissions.realiased(permission, old_alias, new_alias)`
- `#!ts permissions.synced()`

## Notes
- On `permissions.synced`, the core bootstrap permissions `garrysmod.admin` and `garrysmod.superadmin` are ensured, then groups are re-synced.
- Changes are broadcast with interlink channels under `database.permissions:*` and reflected on receivers if event timestamps are newer than local `sync_time`.

## References

- [Variables - Permissions](variables/permissions.md): Shared realm and networked permissions.