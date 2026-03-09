# Command System
This is a highly adaptive command system that allows you to create unique ways of execution from a user perspective.

## Command Authoring

Commands are built by creating groups and attaching commands:

```lua
local group = BSA.Commands:group("fun")
	:description("Fun commands")
	:flattenize(true) -- flatten this down to root, you can still do `fun slay` however.

group:add("slay")
	:alias("kill")
	:permission("command.fun.slay")
	:argument("player", {})
	:callback(function(invoker, targets)
		-- implementation
	end)
```

While you don't have to create a group and just add it directly on root, it is recommended to be within a group.

## Interface Layer

Input routes are implemented as interfaces:

- `chat`: chat prefixes (`sv_chat.lua`)
- `console`: console command entry (`sv_console.lua`)
- `instant`: spawnmenu-style instant execution (`sv_instant.lua`)
- `interface`: UI/network interface execution (`sv_interface.lua`)
- `lua`: server-side direct execution helpers (`sv_server.lua`)

Each interface:

- builds an invoker handle (`interface:handle(...)`)
- attaches cached identity/group data (`_username`, `_identifier`, `_groups`, ...)
- optionally enforces ratelimits/silent rules
- calls `interface:invoke(handle, message)`

## Related Docs

- [Command Structure](structure.md): player-facing argument syntax and examples.
- [Command Interface](interface.md): developer contract for creating in-server and serverless interfaces.
