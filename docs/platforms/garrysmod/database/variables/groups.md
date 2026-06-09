# {{ realm("shared") }} Variables: Groups
Replicated group state layer (`bsa_groups`) exposed as `BSA.Groups`, with helper APIs for inheritance, targeting, and permission aggregation.

!!! info
	See [core/database/variables/groups.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/variables/groups.lua) for the actual design implementation.

## Constants
- `#!ts BSA.Groups.SYSTEM = 1`
- `#!ts BSA.Groups.CONSOLE = 2`
- `#!ts BSA.Groups.USER = 3`

## Functions
- `#!ts groups:list(): table`\
Returns numeric list of groups plus name-key lookup table.

- `#!ts groups:get(name_id: string|number): table|false`\
Gets a group by `name` or `group_id`.

- `#!ts groups:color(name_id: string|number): Color`\
Returns group color (fallbacks to user/default white).

- `#!ts groups:inheritances(name_id: string|number|table): table`\
Builds inheritance chain (circular-safe, depth-limited).

- `#!ts groups:cantarget(a: table|group, b: table|group, ...permissions: string): boolean, string?`\
Authority check comparing primary weights and optional permission-scope weights.

- `#!ts groups:getpermissions(groups: table|group): table`\
Aggregates all direct + inherited permissions; returns both `perm_id -> name` and `name -> perm_id` keys.

- `#!ts groups:getauthority(groups: table|group): number, group?`\
Returns primary group authority tuple.

- `#!ts groups:gethighestauthority(groups: table|group): number, group?`\
Returns highest authority across all supplied groups.

- `#!ts groups:haspermission(groups: table|group, ...permissions: string|number): boolean, table?`\
Requires all permissions; second return is missing list when false.

- `#!ts groups:hasanypermission(groups: table|group, ...permissions: string|number): boolean`\
True when any requested permission exists.

- `#!ts groups:getpermissionweight(groups: table|group, permission: string|number): number`\
Returns maximum effective weight for that permission.

## Group Permission Helpers (`groups.Permissions`)
- `#!ts groups.Permissions:has(group: number|table, permission: number|string|table): table|false`
- `#!ts groups.Permissions:weight(group: number|table, permission: number|string|table): number|false`
- `#!ts groups.Permissions:list(group: number|table, recursive?: boolean): table`

## Runtime Events
- `#!ts groups.added(group: table)`\
	Fired after a group is inserted into the replicated registry and registered with CAMI (when applicable).

- `#!ts groups.removed(group: table)`\
	Fired after a group is evicted from the replicated registry and unregistered from CAMI (when applicable).

- `#!ts groups.updated(group: table)`\
	Fired when an existing group's data changes in the registry without being added or removed (e.g. weight, color, alias, inheritance).

## Hooks
GMod hooks fired alongside the dispatcher events above.\
Dispatchers are always first-order and used internally by BSA.

- `#!ts BSA.Groups:added(group: table)`\
	Fired after a group is added to the registry and registered with CAMI (when applicable).

- `#!ts BSA.Groups:removed(group: table)`\
	Fired after a group is removed from the registry and unregistered from CAMI (when applicable).

- `#!ts BSA.Groups:updated(group: table)`\
	Fired when an existing group entry changes (not added or removed).