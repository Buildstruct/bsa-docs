# {{ realm("shared") }} Variables: Players
Replicated per-player state and player-facing helper API exposed through `BSA.Players` and patched onto the `Player` metatable.

!!! info
	See [core/database/variables/players.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/variables/players.lua) for the actual design implementation.

## Runtime Events
- `#!ts players.uided(entity: Player)`\
  Fired once when `bsa_uid` is first set — the player's internal `player_id` is now available.

- `#!ts players.aided(entity: Player)`\
  Fired once when `bsa_aid` is first set — the player's `account_id` is now available.

- `#!ts players.initialized(entity: Player)`\
  Fired once when `bsa_initialize` is first set — BSA has finished setting up all per-player state.

- `#!ts players.sessioned(entity: Player, id: number)`\
  Fired when the player is assigned a unique session ID for this connection.

- `#!ts players.connected(steamid64: string, session_id: number, player?: Player)`\
  Fired when a player's BSA connection event is recorded.\
  `player` may be `nil` on the client if the entity is not yet resolvable by SteamID64.

- `#!ts players.disconnected(steamid64: string, session_id: number, player?: Player)`\
  Fired when a player's BSA disconnection event is recorded.

- `#!ts players.primaried(entity: Player, old_group: table, new_group: table)`\
  Fired when `bsa_primary` changes.\
  Both arguments are resolved group tables.

- `#!ts players.secondaried(entity: Player, old_groups: table, new_groups: table)`\
  Fired when `bsa_secondary` changes.\
  Both arguments are tables of resolved group entries.

- `#!ts players.afked(entity: Player, state: boolean)`\
  Fired when a player's AFK state changes.\
  `state` is `true` when going AFK, `false` on return.

- `#!ts players.faked(entity: Player, ent_index: number, name?: string, color?: Color)`\
  Fired when a player's displayed group name is overridden via `SetFakeGroup`.\
  `name` and `color` are `nil` when the override is cleared.

- `#!ts players.disguised(entity: Player, ent_index: number, disguise_name?: string)`\
  Fired when `SetDisguise` is applied or cleared.\
  `disguise_name` is `nil` on clear.

## Hooks
GMod hooks fired alongside the dispatcher events above.

- `#!ts BSA.Players:connected(steamid64, session_id, player?)`
- `#!ts BSA.Players:disconnected(steamid64, session_id, player?)`
- `#!ts BSA.Players:sessioned(entity, id)`
- `#!ts BSA.Players:primaried(entity, old_group, new_group)`
- `#!ts BSA.Players:secondaried(entity, old_groups, new_groups)`
- `#!ts BSA.Players:disguised(entity, ent_index, disguise_name?)`
- `#!ts BSA.Players:faked(entity, ent_index, name?, color?)`
- `#!ts BSA.Players:afked(entity, state)`

## Core Player Methods

### Identity

- `#!ts player:GetUID(): number`\
  Returns the player's internal `player_id` from `bsa_players`.\
  Returns `-1` if not yet set.

- `#!ts player:GetAID(): number`\
  Returns the player's `account_id` from `bsa_accounts`.\
  Alias: `GetACC`.

- `#!ts player:GetCreated(): number`\
  Returns the account creation timestamp as a Unix timestamp.

### Groups

- `#!ts player:GetUserGroup(absolute?: boolean, not_disguise?: boolean): string | table`\
  Returns the primary group.\
  Without `absolute`, returns the group name string.\
  With `absolute`, returns the full group table.\
  If `not_disguise` is false (or CLIENT for other players), the disguise primary is applied.

- `#!ts player:GetUserGroupAlias(not_disguise?: boolean): string`\
  Returns the primary group's display alias.\
  Alias: `GetPrimaryGroupAlias`.

- `#!ts player:GetUserGroupColor(not_disguise?: boolean): Color`\
  Returns the primary group's color.\
  Falls back to `color_white` if not found.

- `#!ts player:GetUserGroups(absolute?: boolean, not_disguise?: boolean): table`\
  Returns all groups (primary + secondaries) as an array.\
  Also keyed by group name.\
  Alias: `GetAllGroups`.

- `#!ts player:GetSecondaryGroups(absolute?: boolean, not_disguise?: boolean): table`\
  Returns secondary groups only, without the primary.\
  Array-only, not keyed.

- `#!ts player:GetHighestGroup(absolute?: boolean, not_disguise?: boolean): string | table`\
  Returns the single highest-weight group across all the player's groups.

- `#!ts player:GetHighestGroupAlias(): string`\
  Returns the alias of the highest-weight group.

- `#!ts player:IsUserGroup(...group_names: string): boolean`\
  Returns `true` only if the player has **all** of the named groups.\
  Alias: `HasUserGroup`.

### Display overrides

- `#!ts player:SetDisguise(name?: string, time?: number, primary?: number, secondaries?: number[])`\
  SERVER only.\
  Applies an identity disguise: overrides the player's visible name, displayed time, and group.\
  Pass `nil` for `name` to clear the disguise.

- `#!ts player:SetFakeGroup(name?: string, color?: Color)`\
  SERVER only.\
  Overrides only the player's displayed group label and color without affecting actual group data.\
  Pass `nil` for `name` to clear.

- `#!ts player:IsFakeGroup(): string | false, Color`\
  Returns the current fake group name (or `false`) and its color.\
  Alias: `GetFakeGroup`.

- `#!ts player:GetDisplayGroup(absolute?: boolean): string, Color`\
  Returns what should be rendered as the player's group label.\
  Returns the fake group name and color if one is set, otherwise falls back to the highest real group alias and color.

- `#!ts player:GetDisplayGroupColor(absolute?: boolean): Color`\
  Returns just the display color — the fake group color if set, otherwise the highest real group color.

### Permissions + authority

- `#!ts player:HasPermission(...permissions): boolean`\
  Returns `true` if the player holds **all** of the given permissions across any of their groups.\
  Aliases: `HasPermissions`.

- `#!ts player:HasAnyPermission(...permissions): boolean`\
  Returns `true` if the player holds **at least one** of the given permissions.\
  Aliases: `HasAnyPermissions`.

- `#!ts player:GetPermissions(absolute?: boolean): table`\
  Returns all permissions held by the player's groups.

- `#!ts player:GetPermissionWeight(permission: string | number): number`\
  Returns the weight of the highest group that grants the given permission.

- `#!ts player:CanTarget(target: Player, ...permissions): boolean`\
  Returns `true` if this player's authority is higher than the target's, optionally also checking that this player holds the given permissions.

- `#!ts player:GetWeight(not_disguise?: boolean): number`\
  Returns the primary group's weight value.\
  Aliases: `GetImmunity`, `GetAuthority`.

### Time + AFK

- `#!ts player:GetPlayTime(absolute?: boolean): number`\
  Returns total playtime in seconds.\
  Accounts for AFK pausing and disguise time on the client.

- `#!ts player:GetSessionTime(): number`\
  Returns seconds elapsed since this player's current session started (since `bsa_initialize` was set).

- `#!ts player:GetSessionID(): number`\
  Returns the player's current session ID.

- `#!ts player:SetAFK(state: boolean)`\
  Sets the player's AFK state.\
  Freezes or resumes the playtime offset accordingly.

- `#!ts player:GetAFK(): boolean`\
  Returns whether the player is currently AFK.\
  Alias: `IsAFK`.

- `#!ts player:GetAFKTime(absolute?: boolean): number`\
  Returns how long the player has been AFK in seconds.\
  Returns `0` if not AFK.

### Status

- `#!ts player:IsInitialized(): boolean`\
  Returns `true` once BSA has finished setting up the player (`bsa_initialize` is set).

- `#!ts player:IsAdmin(): boolean`\
  Returns `true` if the player has `garrysmod.admin` or `garrysmod.superadmin`.

- `#!ts player:IsSuperAdmin(): boolean`\
  Returns `true` if the player has `garrysmod.superadmin`.

### Naming

- `#!ts player:Nick(...): string`\
  Overrides the default `Nick`.\
  Returns the censor replacement, renick, or disguise name when applicable — otherwise the real name.

- `#!ts player:Name(...): string`\
  Same override logic as `Nick`.\
  Both are kept in sync.

- `#!ts player:RealName(...): string`\
  Returns the player's actual name, bypassing all overrides.

## Global Player Filters

- `#!ts player.GetByPermission(...permissions): Player[]`\
  Returns all players who hold **all** of the given permissions.\
  Alias: `GetByPermissions`.

- `#!ts player.GetByAnyPermission(...permissions): Player[]`\
  Returns all players who hold **at least one** of the given permissions.

- `#!ts player.GetByGroup(...group_names): Player[]`\
  Returns all players who are in **all** of the given groups.\
  Alias: `GetByGroups`.
