# Creating a Plugin
This guide documents the plugin authoring pattern used by the Garry's Mod BSA platform.

If you only need the raw manager API and lifecycle details, see [Plugin Runtime Reference](reference.md).

## Start With The Right Layout

Use a top-level file when the plugin is small:

```text
lua/bsa/plugins/sh_myplugin.lua
```

Use a folder when the server and client parts are substantial:

```text
lua/bsa/plugins/myplugin/
  sh_init.lua
  sv_init.lua
  cl_init.lua
```

The loader supports both forms. Folder plugins are the better choice once the client interface or networking becomes non-trivial, as shown by `logging`.

## Step 1: Define And Register The Plugin

Every plugin starts as a plain Lua table and is registered with `BSA.Plugins:add(name, plugin)`.

```lua
local plugin = {}
plugin.description = "Controls flashlight usage through BSA permissions."
plugin.config = {
    alias = "Flashlight",
    permissions = {"management.flashlight"},
    sync = true
}
plugin.client_config = {
    alias = "Flashlight",
    permissions = {"*"}
}
plugin.language = {
    alias = "Flashlight"
}
plugin.permissions = {
    "utility.flashlight"
}
```

What these fields are for:

- `description` is descriptive metadata for the plugin.
- `config` seeds the top-level `config.Plugins.<name>` toggle node.
    - setting sync to true allows the config to be networked to clients.
- (Optional) `client_config` seeds `config.Client.Plugins.<name>` when the plugin is enabled on the client.
- (Optional) `language` seeds `config.Language.Plugins.<name>` when the plugin is enabled.
- (Optional) `permissions` is a list of permission IDs the plugin introduces. These are registered while enabling when interlink is available.

The registration name should stay stable.\
Renaming the plugin changes its config path and persisted file name.

## Step 2: Build Runtime State In `constructor`

`plugin:constructor()` runs every time the plugin is enabled. Treat it as runtime setup, not static module initialization.

```lua
function plugin:constructor()
    self.language:add("string", "denied", {
        default = "You do not have permission to use flashlight."
    })

    self.cfg_enforce = self.config:add("boolean", "enforce", {
        alias = "Enforce",
        description = "Require utility.flashlight before allowing flashlight usage.",
        default = true
    })
end
```

During enable, BSA gives your plugin instance these containers:

- `self.config` for runtime plugin config
- `self.language` for plugin-local language/config phrases
- `self.client_config` on the client only

## Step 3: Use Tracked Hooks, Timers, and Dispatchers

Use `self:add_hook(...)` instead of raw `hook.Add(...)`. Timers, dispatcher connections, and HTTP requests are also tracked — see [Plugin Runtime Reference](reference.md) for the full surface.

```lua
function plugin:constructor()
    self:add_hook("PlayerSwitchFlashlight", self:id(), function(invoker, enabled)
        if not self.cfg_enforce:get() then
            return
        end

        if BSA.Players.HasPermission(invoker, "utility.flashlight") then
            return true
        end

        return false
    end)
end
```

Hook IDs are automatically namespaced as `<plugin>.<id>`. Everything registered this way is cleaned up automatically on disable through `plugin:clean()`.

## Step 4: Clean Up What Is Not Tracked

Tracked: hooks, timers (`add_timer`/`simple_timer`), dispatcher connections (`add_dispatcher`), and HTTP requests (`self:http`). These are released automatically on disable.\
Not tracked: raw `network:receive(...)`, file handles, global state your plugin mutated.

```lua
function plugin:destructor()
    network:receive("plugin.flashlight.sync", nil)
end
```

## Step 5: Add Language Phrases

`self.language` is created for every enabled plugin and supports nested phrase trees.

```lua
function plugin:constructor()
    do local notifications = self.language:add("container", "notifications")
        notifications:add("string", "denied", {
            default = "Flashlight usage is not allowed."
        })
    end
end
```

Then fetch text with:

```lua
self.language:phrase("#notifications.denied")
```

- `#path.to.phrase` resolves through the plugin language tree.
- Extra arguments are passed through `string.format`.
- The language tree exists on both server and client.

## Step 6: Add Client Config Or Interface When Needed

`plugin.client_config` is only materialized into a config container on the client during enable.

That means `self.client_config:add(...)` should only be used from client code or behind `if CLIENT then`.

For interface-heavy plugins, define `plugin.interface` and keep the implementation clientside.

```lua
do local interface = {}
    plugin.interface = interface
    interface.alias = "Flashlight"
    interface.icon = "icon16/lightbulb.png"
    interface.permissions = {"utility.flashlight"}

    function interface:constructor(parent)
        -- build VGUI here
    end

    function interface:destructor()
    end
end
```

When the plugin enables on the client, BSA mounts that interface through `BSA.Interface:add(name, interface)`.\
See [Interface Overview](../../interface/index.md) for how interfaces are handle and their functions.\
See [Interface Overview - Feature](../../interface/index.md#base-feature-class-interfacebase) about the structure of the interface table.

## Step 7: Support Realm Separation Deliberately

A few rules make plugin authoring less error-prone:

- Put server-only storage, database, or authoritative logic in `sv_*.lua` or `sv_init.lua`.
- Put large VGUI and client presentation code in `cl_*.lua` or `cl_init.lua`.
- If you split the plugin by realm, register the same plugin name in each realm entry file.

## Full Example

```lua
local plugin = {}
plugin.description = "Controls flashlight usage through BSA permissions."
plugin.config = {
    alias = "Flashlight",
    permissions = {"management.flashlight"},
    sync = true
}
plugin.client_config = {
    alias = "Flashlight",
    permissions = {"*"}
}
plugin.permissions = {
    "utility.flashlight"
}

function plugin:constructor()
    self.language:add("string", "denied", {
        default = "You do not have permission to use flashlight."
    })

    self.cfg_enforce = self.config:add("boolean", "enforce", {
        alias = "Enforce",
        description = "Require utility.flashlight before allowing flashlight usage.",
        default = true
    })

    self:add_hook("PlayerSwitchFlashlight", self:id(), function(invoker, enabled)
        if not self.cfg_enforce:get() then
            return
        end

        if BSA.Players.HasPermission(invoker, "utility.flashlight") then
            return true
        end

        return false
    end)
end

function plugin:destructor()
    network:receive("plugin.flashlight.sync", nil)
end

BSA.Plugins:add("flashlight", plugin)
```

## Common Mistakes

- Using raw `hook.Add(...)` and forgetting cleanup.
- Calling `self.client_config:add(...)` from shared/server code.
- Renaming a plugin after shipping it and then wondering why old config is not picked up.
- Forgetting to unregister `network:receive(...)` in `destructor()` — this is the main thing not auto-cleaned.