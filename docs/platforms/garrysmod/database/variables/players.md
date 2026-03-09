# Variables: Players
Replicated per-player state and player-facing helper API exposed through `BSA.Players` and patched onto the `Player` metatable.

## Runtime Events
- `#!ts players.initialized(entity: Player)`
- `#!ts players.connected(steamid64: string, player?: Player)`
- `#!ts players.disconnected(steamid64: string, player?: Player)`
- `#!ts players.faked(entity: Player, ent_index: number, name?: string, color?: Color)`
- `#!ts players.disguised(entity: Player, ent_index: number, disguise_name?: string)`
- `#!ts players.primaried(entity: Player, old_group, new_group)`
- `#!ts players.secondaried(entity: Player, old_groups: table, new_groups: table)`
- `#!ts players.afked(entity: Player, state: boolean)`

## Core Player Methods
Group + identity:

- `#!ts player:GetUserGroup(absolute?: boolean, not_disguise?: boolean): string|table`
- `#!ts player:GetUserGroupAlias(not_disguise?: boolean): string|nil`
- `#!ts player:GetUserGroupColor(not_disguise?: boolean): string|nil`
- `#!ts player:GetUserGroups(absolute?: boolean, not_disguise?: boolean): table`
- `#!ts player:GetSecondaryGroups(absolute?: boolean, not_disguise?: boolean): table`
- `#!ts player:GetHighestGroup(absolute?: boolean, not_disguise?: boolean): string|table`
- `#!ts player:GetHighestGroupAlias(): string`
- `#!ts player:IsUserGroup(...group_names: string): boolean`

Display overrides:

- `#!ts player:SetDisguise(name?: string, time?: number, primary?: number, secondaries?: number[]): void`
- `#!ts player:SetFakeGroup(name?: string, color?: Color): void`
- `#!ts player:IsFakeGroup(): string|false, Color`
- `#!ts player:GetDisplayGroup(absolute?: boolean): string, Color`

Permission + authority:

- `#!ts player:GetPermissions(absolute?: boolean): table`
- `#!ts player:GetPermissionWeight(permission: string|number): number`
- `#!ts player:HasPermission(...permissions): boolean, table?`
- `#!ts player:HasAnyPermission(...permissions): boolean`
- `#!ts player:CanTarget(target: Player, ...permissions): boolean, string?`
- `#!ts player:GetWeight(not_disguise?: boolean): number`\
Aliases: `GetImmunity`, `GetAuthority`, `HasPermissions`, `HasAnyPermissions`.

Time + AFK:

- `#!ts player:GetPlayTime(absolute?: boolean): number`
- `#!ts player:GetSessionTime(): number`
- `#!ts player:SetAFK(state: boolean): void`
- `#!ts player:GetAFK(): boolean`
- `#!ts player:GetAFKTime(absolute?: boolean): number`
- `#!ts player:IsInitialized(): boolean`

Admin checks + naming:

- `#!ts player:IsAdmin(): boolean`
- `#!ts player:IsSuperAdmin(): boolean`
- `#!ts player:Nick(...): string`
- `#!ts player:Name(...): string`
- `#!ts player:RealName(...): string`

## Global Player Filters
- `#!ts player.GetByPermission(...)`
- `#!ts player.GetByAnyPermission(...)`
- `#!ts player.GetByGroup(...)`
