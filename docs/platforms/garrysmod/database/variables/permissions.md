# {{ realm("shared") }} Variables: Permissions
Replicated permission registry (`bsa_permissions`) exposed as `BSA.Permissions`, including CAMI bridge hooks.

!!! info
	See [core/database/variables/permissions.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/variables/permissions.lua) for the actual design implementation.

## Functions
- `#!ts permissions:get(name_id: string|number): table|false`\
Gets permission by `name` or `perm_id`.

- `#!ts permissions:add(name: string, alias?: string, callback?: function)`\
Server-only passthrough to `BSA.Storage.Permissions:add(...)`.

- `#!ts permissions:remove(name_id: string|number, callback?: function)`\
Server-only passthrough to `BSA.Storage.Permissions:remove(...)`.

- `#!ts permissions:player(...permissions: string|number): Player[]`\
Returns connected players matching all requested permissions.

## Runtime Events
- `#!ts permissions.added(permission)`
- `#!ts permissions.removed(permission)`

## CAMI Integration
- Server bridges `CAMI.OnPrivilegeRegistered` / `CAMI.OnPrivilegeUnregistered` to `bsa_permissions` entries prefixed with `cami.`.
- `CAMI.PlayerHasAccess` delegates to BSA permission checks and targeting logic (`BSA.Players.HasPermission` / `BSA.Players.CanTarget`).
