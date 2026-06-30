# {{ realm("server") }} Command System
This is a highly adaptive command system that allows you to create unique ways of execution from a user perspective.

## Command Authoring

Commands are built by creating groups and attaching commands.

```lua
local group = BSA.Commands:group("fun")
	:description("Fun commands")
	:flattenize() -- flatten this down to root, you can still do `fun slay` however.

group:add("slay")
	:alias("kill")
	:permission("command.fun.slay")
	:argument("player", {})
	:callback(function(invoker, targets)
		-- implementation
	end)
```

While you don't have to create a group and just add it directly on root, it is recommended to be within a group.

`flattenize()` takes no arguments.\
`group:add(name)` is an alias of `group:command(name)`.

## Asynchronous Logic

Command callbacks and argument resolvers run inside a coroutine, so you can suspend on async work (a DB read, a permission check) and resume with the result.\
Use `invoker:await(fn)` (or `BSA.Commands:await(fn)`), where `fn(resolve)` drives the callback, `await` returns whatever you pass to `resolve`.

```lua
group:add("balance")
	:callback(function(invoker)
		local value = invoker:await(function(resolve)
			BSA.Currency:get(invoker.entity, "credits", resolve)
		end)
		invoker:reply("You have " .. value:toString())
	end)
```

Await throws if not resolved within the timeout (30s by default).\
`invoker:can`, `invoker:has`, and `invoker:scope` are dual-mode, pass a callback for CPS style, or omit it to await the result inline.

## Interface Layer

Input routes are implemented as interfaces:

- `chat`: chat prefixes (`sv_chat.lua`)
- `console`: console command entry (`sv_console.lua`)
- `instant`: spawnmenu-style instant execution (`sv_instant.lua`)
- `interface`: UI/network interface execution (`sv_interface.lua`)
- `lua`: server-side direct execution helpers (`sv_lua.lua`)

Client-side console and Lua interfaces (`cl_console.lua`, `cl_lua.lua`) and the shared autocomplete layer (`sh_autocomplete.lua`) extend this on the client realm.

Each interface:

- builds an invoker handle (`interface:handle(...)`)
- attaches cached identity/group data (`_username`, `_identifier`, `_groups`, ...)
- optionally enforces ratelimits/silent rules
- calls `interface:invoke(handle, message)`

## Related Docs

- [Command Structure](structure.md): player-facing argument syntax and examples.
- [Command Interface](interface.md): developer contract for creating in-server and serverless interfaces.
