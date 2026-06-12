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

- `#!ts logging:metadata(name: string, alias: string)`

!!! warning
	Do not call `metadata()` inside a hook callback or per-event code path.\
	Call it once during plugin enable.

Registers a metadata category with the logging plugin.\
This creates config nodes for copying notifications and context menus.

---

- {{ realm("server") }} `#!ts logging:emit(cfg: configurate.proxy | string, msg: repr.object, meta?: table, options?: table): table`

Emits a log entry to be stored and uploaded for administrators.\
The meta table expects a name & value array `{name: string, value: string}` if used.\
Meta tables should be properly populated for searching capabilities.

The options table is an additional set to be passed into how logs are processed.

| Key | Type | Description |
|---|---|---|
| `exclude` | `Player | any` | Exclude this player/entity from network delivery. Useful to avoid echoing a message back to its invoker. |
| `silent` | `boolean` | When `true`, restricts network delivery to players who have both `utility.logging` **and** `commands.silent.visible`. |
| `send_players` | `boolean | Entity` | Set to `false` to suppress all player delivery. Defaults to the category's `players` config value. |
| `interface_recipients` | `Player[]?` | Explicit recipient list for interface pushes. When `nil`, sends to all players with `utility.logging`. |

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

The following shows a complete integration from an external plugin. It registers a custom category during the logging enable event, then emits a record whenever something relevant happens.

```lua
-- add this hook shared
local category
hook.Add("BSA.Plugins:enable", "Sample", function(name, plugin)
	if name ~= "logging" then return end
	logging:metadata("sample_meta", "Sample Meta")
	category = logging:category("sample", "Sample", Color(0, 200, 255))
end)

-- add this hook server-side
hook.Add("Example", "sample", function(some_player, some_string)
	if not BSA.Logging then return end
	if not category:get() then return end -- likely disabled
	local logging = BSA.Logging

	-- create our message throught REPR
	local msg_instruct = logging:repr(some_player, " (" .. some_player:SteamID64() .. ") did " .. some_string)

	-- emit it under "sample" category with some metadata
	logging:emit("sample", msg_instruct, {
		{name = "username", value = some_player:Nick()},
		{name = "identifier", value = some_player:SteamID64()},
		{name = "sample_meta", value = some_string}
	}, {
		-- we can make it so that if they can see logs, they don't see their own networked to them.
		exclude = some_player
	})
end)
```