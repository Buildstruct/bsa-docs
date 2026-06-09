# {{ realm("shared") }} Variables: Punishments
Punishment variable bridge for player runtime state.\
This layer maps active storage punishments to per-player replicated variables and provides type-specific runtime checks.

!!! info
	See [core/database/variables/punishments.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/variables/punishments.lua) for the actual design implementation.\
	See [core/database/punishments](https://github.com/Buildstruct/bsa-platform-gmod/tree/develop/lua/bsa/core/database/punishments) for punishment type implementations.

## Shared Helper
- `#!ts BSA.Punishments.format(entry, type?: string): string?`\
	Builds configured punishment message using scope-specific aspect text and placeholders (`id`, `aspect`, `created`, `expires`, `duration`, `invoker`, `reason`).

---

## Type: Ban
Server behavior only.

- On punishment `added`/`applied`, immediately kicks target with formatted message.
- `CheckPassword` gate denies entry when active ban is found.

---

## Type: Censor

### Runtime Events
- `#!ts punishments.Censor.added(entity: Player, entry: table)`
- `#!ts punishments.Censor.removed(entity: Player, entry: table)`
- `#!ts punishments.Censor.updated(entity: Player, old_entry: table, new_entry: table)`

### Hooks
- `#!ts BSA.Punishments.Censor:added(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Censor:removed(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Censor:updated(entity: Player, old_entry: table, new_entry: table)`

### Player Helper
- `#!ts player:IsCensor(): table | false`\
	Alias exported as `punishments.IsCensor`.

### Effects
- Syncs from storage punishment lifecycle (`added`, `updated`, `revoked`, `removed`, `expired`, `applied`, `invalidated`).
- Chat replacement via `PlayerSay` when `auto_mute` is enabled.
- Voice blocked via `PlayerCanHearPlayersVoice` / client `PlayerStartVoice` when `auto_gag` is enabled.

---

## Type: Gag

### Runtime Events
- `#!ts punishments.Gag.added(entity: Player, entry: table)`
- `#!ts punishments.Gag.removed(entity: Player, entry: table)`
- `#!ts punishments.Gag.updated(entity: Player, old_entry: table, new_entry: table)`

### Hooks
- `#!ts BSA.Punishments.Gag:added(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Gag:removed(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Gag:updated(entity: Player, old_entry: table, new_entry: table)`

### Player Helper
- `#!ts player:IsGag(): table | false`\
Alias exported as `punishments.IsGag`.

### Effects
- Syncs from storage punishment lifecycle.
- Voice blocked server-side (`PlayerCanHearPlayersVoice`) and client-side (`PlayerStartVoice`).

---

## Type: Limbo

### Runtime Events
- `#!ts punishments.Limbo.added(entity: Player, entry: table)`
- `#!ts punishments.Limbo.removed(entity: Player, entry: table)`
- `#!ts punishments.Limbo.updated(entity: Player, old_entry: table, new_entry: table)`

### Hooks
- `#!ts BSA.Punishments.Limbo:added(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Limbo:removed(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Limbo:updated(entity: Player, old_entry: table, new_entry: table)`

### Player Helpers
- `#!ts player:IsLimbo(): table | false`\
	Aliases: `IsBanished`, `IsBanned`, `IsPlear` and exported on `punishments.Limbo`.

### Extra API
- `#!ts punishments.Limbo.Debuff(player)`\
	Applies heavy movement/combat restrictions.

### Effects
- Syncs from storage punishment lifecycle.
- Optional hard-kick mode (`auto_kick`) on add/apply/login.
- When active (non-kick mode): strips weapons/ammo, enforces debuffs, blocks many gameplay actions/commands/hooks, blocks damage output, and can block chat/voice based on config.

---

## Type: Mute

### Runtime Events
- `#!ts punishments.Mute.added(entity: Player, entry: table)`
- `#!ts punishments.Mute.removed(entity: Player, entry: table)`
- `#!ts punishments.Mute.updated(entity: Player, old_entry: table, new_entry: table)`

### Hooks
- `#!ts BSA.Punishments.Mute:added(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Mute:removed(entity: Player, entry: table)`
- `#!ts BSA.Punishments.Mute:updated(entity: Player, old_entry: table, new_entry: table)`

### Player Helper
- `#!ts player:IsMute(): table | false`\
	Alias exported as `punishments.IsMute`.

### Effects
- Syncs from storage punishment lifecycle.
- Blocks chat messages (`OnPlayerChat` and `PlayerSay` path in server module).

---

## Type: Warn.

### Effects
- Syncs from storage punishment lifecycle.
- `auto_ban` temporarily stops connections until active warns reduce bellow the `threshold`.
- `auto_kick` removes a user after a `threshold` is reached, which can be made `consecutive` if needed.