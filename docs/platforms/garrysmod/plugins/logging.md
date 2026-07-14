# {{ state("public") }} {{ realm("shared") }} Logging
A multi-use log system for administrators to view events that have transpired.\
Supports flat-file storage, SQL deep-storage, and real-time interface delivery.

!!! note
	This adds a dedicated table to BSA under `Logging` when enabled.

## Functions

- `#!ts logging:category(tag: string, alias: string, color: Color, log_only?: boolean): configurate.proxy`

!!! warning
	Do not call `category()` inside a hook callback or per-event code path.\
	Call it once during plugin enable.

Registers a new log category with the logging plugin.\
This creates configurations that lets administrators enable/disable the category and tune its output targets.

---

- {{ realm("server") }} `#!ts logging:emit(cfg: configurate.proxy | string, msg: repr.object, meta?: table, options?: table): table`

Emits a log entry to be stored and uploaded for administrators.\
Metadata requires no registration, pass it directly on `emit`.\
See [Metadata](#metadata) for the accepted forms.\
Populate metadata well so records remain searchable.

The options table is an additional set to be passed into how logs are processed.

| Key | Type | Description |
|---|---|---|
| `exclude` | `Player | any` | Exclude this player/entity from network delivery. Useful to avoid echoing a message back to its invoker. |
| `silent` | `boolean` | When `true`, restricts network delivery to players who have both `utility.logging` **and** `commands.silent.visible`. |
| `send_players` | `boolean | Entity` | Set to `false` to suppress all player delivery. Defaults to the category's `players` config value. |
| `interface_recipients` | `Player[]?` | Explicit recipient list for interface pushes. When `nil`, sends to all players with `utility.logging`. |

---

## Metadata

Metadata is language-agnostic: the display label is derived from the key and the semantic type is detected from the value. There is no per-key registration.

`emit` accepts either form:

```lua
-- hash form (simplest) — keys ordered alphabetically in the interface
logging:emit("chat", msg, {
    username = ply:Nick(),
    identifier = ply:SteamID64(), -- detected as an identifier
    message = text,
    silent = false, -- boolean -> flag, hidden from the copy menu
})

-- array form — preserves order, and allows an explicit type override
logging:emit("chat", msg, {
    {name = "username", value = ply:Nick()},
    {name = "identifier", value = ply:SteamID64()},
    {name = "message", value = text},
})
```

**Labels** are humanized from the key: `old_name` → "Old Name", `attacker_identifier` → "Attacker ID" (common acronyms like `id`/`ip`/`url` are upper-cased).

**Types** are auto-detected and drive interface behavior:

| Type | Detected from | Interface behavior |
|---|---|---|
| `identifier` | key `identifier` or ending in `_identifier` | Copyable, exposes player actions (time, groups, punishments). |
| `flag` | a boolean value (or the string `"true"`/`"false"`) | Hidden from the copy menu. |
| `number` | a number value | Copyable. |
| `text` | anything else (default) | Copyable. |

Pass `type` on an array entry to override detection. Types are derived, not stored, `bsa_logging_meta` keeps only `name` and `value`, and deep-storage rows re-derive their type on read.

---

## Built-in Categories

The following categories are registered by the logging plugin itself.\You can reference these by their tag name string when filtering in the interface.

| Tag | Alias | Color | Key Meta Fields |
|---|---|---|---|
| `commands` | Commands | Red | `username`, `identifier`, `command`, `silent` |
| `chat` | Chat | Blue | `username`, `identifier`, `message` |
| `name` | Name | Blue | `username`, `identifier`, `old_name`, `new_name` |
| `connections` | Connections | Blue | `username`, `identifier`, `address` / `reason` |
| `objects` | Objects | Green | `username`, `identifier`, `model` |
| `props` | Props | Green | `username`, `identifier`, `model` |
| `effects` | Effects | Red | `username`, `identifier`, `model` |
| `ragdolls` | Ragdolls | Yellow | `username`, `identifier`, `model` |
| `npcs` | NPCs | Purple | `username`, `identifier`, `class` |
| `sents` | SENTs | Purple | `username`, `identifier`, `class` |
| `sweps` | SWEPs | Cyan | `username`, `identifier`, `class` |
| `vehicles` | Vehicles | Orange | `username`, `identifier`, `class` |
| `tools` | Tools | Purple | `username`, `identifier`, `tool`, `class` |
| `duplicators` | Duplicators | Pink | `username`, `identifier` |
| `server` | Server | Green | `map` |

---

## Example

The following shows a complete integration from an external plugin.\
It registers a custom category during the logging enable event, then emits a record whenever something relevant happens.

```lua
-- add this hook shared
local category
hook.Add("BSA.Plugins:enable", "Sample", function(name, plugin)
	if name ~= "logging" then return end
	category = logging:category("sample", "Sample", Color(0, 200, 255))
end)

-- add this hook server-side
hook.Add("Example", "sample", function(some_player, some_string)
	if not BSA.Logging then return end
	if not category:get() then return end -- likely disabled
	local logging = BSA.Logging

	-- create our message throught REPR
	local msg_instruct = logging:repr(some_player, " (" .. some_player:SteamID64() .. ") did " .. some_string)

	-- emit it under "sample" category — labels and types are derived automatically
	logging:emit("sample", msg_instruct, {
		username = some_player:Nick(),
		identifier = some_player:SteamID64(),
		sample_meta = some_string,
	}, {
		-- we can make it so that if they can see logs, they don't see their own networked to them.
		exclude = some_player
	})
end)
```