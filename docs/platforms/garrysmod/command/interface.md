# Command Interface
Interfaces allows the command system to operate on server and non-server related inputs.\
This makes it extremely easy to adapt this system to different forms of inputs like Discord.

## What an Interface Does

An interface converts external input into a command invocation:

1. Create interface: `commands:interface("<name>")`
2. Build invoker handle: `interface:handle(entityOrData)`
3. Attach cached identity/group data (`_username`, `_identifier`, `_groups`, ...)
4. Call: `interface:invoke(handle, message)`

Core implementation lives in `lua/bsa/core/libraries/command.lua` (`commands.interface` class).

## Required Methods

Your interface must provide:

- `reply(invoker, command, ...)`
- `rreply(invoker, command, ...)`
- `message(invoker, command, targets, ...)`
- `rmessage(invoker, command, targets, ...)`
- `username(invoker)`
- `identifier(invoker)`
- `groups(invoker, callback)`
- `primary(invoker, callback)`
- `secondary(invoker, callback)`
- `can(invoker, other, permissions, callback)`
- `has(invoker, permissions, callback)`

Optional but recommended:

- `condition(invoker, command, callback)` global gate
- `failure(invoker, command, err)` user-facing failure formatter
- `error(invoker, command, traceback)` internal error logger

## In-Server Interface Pattern

Use `serverless = false` when the invoker has an actual player entity.

```lua
local commands = BSA.Commands
local interface = commands:interface("mychat")
interface.serverless = false

function interface:reply(invoker, command, ...)
	BSA.Repr.chat(...):watermark():send(invoker.entity)
end

-- implement rreply/message/rmessage + identity/permission methods...

hook.Add("PlayerSay", "MyCommandInterface", function(ply, text)
	if not IsValid(ply) then return end

	local handle = interface:handle(ply)
	handle._username = ply:Name()
	handle._identifier = ply:SteamID64()
	handle._groups = BSA.Players.GetAllGroups(ply, true)
	handle._primary = BSA.Players.GetPrimaryGroup(ply, true)
	handle._secondary = BSA.Players.GetSecondaryGroups(ply, true)

	interface:invoke(handle, text)
	return ""
end)
```

Reference implementations:

- `command/interfaces/sv_chat.lua`
- `command/interfaces/sv_console.lua`
- `command/interfaces/sv_interface.lua`
- `command/interfaces/sv_instant.lua`

## Serverless Interface Pattern

Use `serverless = true` when invoked outside normal player context (HTTP/queue/automation bot).

```lua
local commands = BSA.Commands
local interface = commands:interface("automation")
interface.serverless = true

function interface:reply(invoker, command, ...)
	print("[AUTOMATION]", ...)
end

-- implement required methods against your external identity model...

local function run_as_service(message)
	local handle = interface:handle(false) -- no player entity
	handle._username = "Automation"
	handle._identifier = "AUTOMATION"
	handle._groups = { BSA.Storage.Groups:get("console") }
	handle._primary = BSA.Storage.Groups:get("console")
	handle._secondary = {}
	interface:invoke(handle, message)
end
```

## Behavior Notes

- `command:playeronly(true)` cannot run when `serverless` or no valid entity.
- `command:serveronly(true)` blocks only `serverless` interfaces.
- Player/entity pickers that need an entity (`@`, `^`, `&`) fail for serverless/custom non-entity invokers.
- `invoker:can(...)` / `invoker:has(...)` must be asynchronous-safe (callback-based).
- `interface:invoke(...)` handles command traversal, alias resolution, flattened-group resolution, conditions, and callback execution.

## Guard Rails

Match existing interfaces when possible:

- ratelimit repeated invocations
- check silent permission before allowing silent mode
- block limbo/restricted player states
- standardize error formatting in `failure(...)`

See `sv_chat.lua` and `sv_console.lua` for concrete guard implementations.
