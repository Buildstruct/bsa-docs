# Command Structure
Sample of argument syntaxes used by the BSA command system.

## Invocation Shape

General shape:

```text
<interface-prefix> <group?> <command> [arg1] [arg2] ...
```

Notes:

- Group nesting is supported (`group subgroup command`).
- Some groups use `:flattenize()` so child commands can be called from parent/root scope.
- Quoted values are supported for string-like arguments:
    - `"hello world"` is treated as one argument.
- Last argument may consume the rest of the input when applicable.

## Argument Flags

Common flags available across many argument types:

- `optional = true` allows missing value.
- `default = ...` fallback value when missing/invalid path allows default.
- `alias = "name"` changes usage/help label.
- `min` / `max` numeric bounds where supported.
- `single = true` forces single match for set-based targets.
- `limit = n` max count for set-based targets.
- `filter = "..."` blocks specific picker prefixes for `player`/`entity`.
- `gated = true` (on `player`) filters resolved targets through the invoker's `can` check, dropping any the invoker may not act on.

`options` and `default` may be **functions** instead of static values.\
They are resolved asynchronously at validation time: the function receives `(invoker, callback, flags)` and must call `callback(true, value)` or `callback(false, err)`.\
Use this for option lists that depend on runtime state.

## Built-In Argument Types

### `number`

Parses via `tonumber`.

Examples:

- `125`
- `3.5`

Supports:

- `min`, `max`, `round`, `default`, `optional`

---

### `string`

Raw text (supports quotes and multi-word capture).

Examples:

- `hello`
- `"hello world"`

---

### `select`

Single value from fixed `options`.

Example with options `{ "easy", "hard" }`:

- `easy`

---

### `multi`

Comma-separated values from fixed `options`.

Examples:

- `fire,ice`
- `"fire, ice, lightning"`

Supports:

- `min`, `max`, `default`, `optional`

---

### `boolean`

Truthy only for `1` or `true`, otherwise false/default path.

Examples:

- `1` -> `true`
- `true` -> `true`
- `0` -> `false`

---

### `color`

Formats:

- `R,G,B`
- `R,G,B,A`
- `#RRGGBB`
- `#RRGGBBAA`
- `0xRRGGBB`
- `0xRRGGBBAA`

Examples:

- `255,0,0`
- `255,0,0,128`
- `#00FF00`
- `0x00FF00`

---

### `vector`

Format: `X,Y,Z`\
Example: `0,128,64`

---

### `angle`

Format: `P,Y,R`\
Example: `0,90,0`

---

### `time`

Accepts seconds or tokenized units:

- `s`, `m`, `h`, `d`, `w`, `mo`, `y`

Examples:

- `90`
- `1h 30m`
- `1w2d`

Clamped to max 1 year (`31536000` seconds).

---

### `player`

Target expression parser with set operators:

- `+` union
- `-` difference
- `!` invert

Prefix pickers:

- By default plain text resolves by player name search
- `@` aimed player
- `^` self
- `*` all players
- `$` SteamID/SteamID64/profile-url player lookup
- `#` usergroup
- `%` permission
- `&` radius around invoker (hammer units)
- `?` random player count

Examples:

- `^` - returns yourself
- `@` - returns whoever you look at
- `#admin+^` - all admins and yourself
- `* - #user` - everyone but users
- `?3` - pick 3 random players
- `&500` - pick players within 500 hammer units
- `$STEAM_0:1:12345` - pick player by steamid/steamid64

---

### `entity`

Same expression engine as `player`, but for entities.

Prefix pickers:

- `@` aimed entity
- `^` self entity
- `*` all entities
- `#` class (`ents.FindByClass`)
- `$` entity index
- `&` radius around invoker

Examples:

- `@` - returns whatever you look at
- `#prop_physics` - all prop_physics
- `* - #npc_*` - all entities except npcs
- `$120` - entity index 120

---

### `steam`

Accepts:

- SteamID (`STEAM_X:Y:Z`)
- SteamID64
- `https://steamcommunity.com/profiles/<steamid64>`
- `^` for invoker steamid64

---

## Example Commands

Examples from `content/sv_fun.lua`:

```text
!slap ^ 10
!slay #admin+^
!give ^ weapon_crowbar
!traffic ?2 3
!rank ^ "Moderator" #00AAFF
```

(`!` is only an example prefix, actual prefixes are interface/config dependent.)
