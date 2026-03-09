# Variables: Punishments
Punishment variable bridge for player runtime state. This layer maps active storage punishments to per-player replicated variables and provides type-specific runtime checks.

## Shared Helper
- `#!ts BSA.Punishments.format(entry, type?: string): string?`\
Builds configured punishment message using scope-specific aspect text and placeholders (`id`, `aspect`, `created`, `expires`, `duration`, `invoker`, `reason`).

## Type: Ban
Server behavior only.

- On punishment `added`/`applied`, immediately kicks target with formatted message.
- `CheckPassword` gate denies entry when active ban is found.

## Type: Censor

### Runtime Events
- `#!ts punishments.Censor.added(player, entry)`
- `#!ts punishments.Censor.removed(player, entry)`
- `#!ts punishments.Censor.updated(player, old_entry, new_entry)`

### Player Helper
- `#!ts player:IsCensor(): boolean`\
Alias exported as `punishments.IsCensor`.

### Effects
- Syncs from storage punishment lifecycle (`added`, `updated`, `revoked`, `removed`, `expired`, `applied`, `invalidated`).
- Chat replacement via `PlayerSay` when `auto_mute` is enabled.
- Voice blocked via `PlayerCanHearPlayersVoice` / client `PlayerStartVoice` when `auto_gag` is enabled.

## Type: Gag

### Runtime Events
- `#!ts punishments.Gag.added(player, entry)`
- `#!ts punishments.Gag.removed(player, entry)`
- `#!ts punishments.Gag.updated(player, old_entry, new_entry)`

### Player Helper
- `#!ts player:IsGag(): boolean`\
Alias exported as `punishments.IsGag`.

### Effects
- Syncs from storage punishment lifecycle.
- Voice blocked server-side (`PlayerCanHearPlayersVoice`) and client-side (`PlayerStartVoice`).

## Type: Limbo

### Runtime Events
- `#!ts punishments.Limbo.added(player, entry)`
- `#!ts punishments.Limbo.removed(player, entry)`
- `#!ts punishments.Limbo.updated(player, old_entry, new_entry)`

### Player Helpers
- `#!ts player:IsLimbo(): boolean`\
Aliases: `IsBanished`, `IsBanned`, `IsPlear` and exported on `punishments.Limbo`.

### Extra API
- `#!ts punishments.Limbo.Debuff(player)`\
Applies heavy movement/combat restrictions.

### Effects
- Syncs from storage punishment lifecycle.
- Optional hard-kick mode (`auto_kick`) on add/apply/login.
- When active (non-kick mode): strips weapons/ammo, enforces debuffs, blocks many gameplay actions/commands/hooks, blocks damage output, and can block chat/voice based on config.

## Type: Mute

### Runtime Events
- `#!ts punishments.Mute.added(player, entry)`
- `#!ts punishments.Mute.removed(player, entry)`
- `#!ts punishments.Mute.updated(player, old_entry, new_entry)`

### Player Helper
- `#!ts player:IsMute(): boolean`\
Alias exported as `punishments.IsMute`.

### Effects
- Syncs from storage punishment lifecycle.
- Blocks chat messages (`OnPlayerChat` and `PlayerSay` path in server module).

## Type: Warn
!!! warning
	Warn is currently under design review for how it will be implemented.\
	:tools: We are in the process of getting this section constructed. :tools: