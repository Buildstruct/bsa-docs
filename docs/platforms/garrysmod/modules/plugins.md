# Plugins
BSA plugins are toggleable feature modules that register themselves with `BSA.Plugins:add(...)` and then participate in a managed lifecycle.

!!! info
	See [core/modules/plugins.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/modules/plugins.lua) for the actual design implementation.

- See [Creating a Plugin](plugins/creating.md) for the practical authoring guide.
- See [Plugin Runtime Reference](plugins/reference.md) for loader behavior, lifecycle, sync, and the manager API.

## What The Plugin System Gives You

- A per-plugin enable toggle under `config.Plugins.<name>`.
- A fresh plugin instance every time the plugin is enabled.
- Automatic hook cleanup when you use `self:add_hook(...)`.
- Per-plugin language/config containers created during enable.
- Server to client syncing of active plugin state.
- Persistent plugin config storage in `data/bsa/config/plugins/<name>.dat`.

## Plugin Shapes

You can author plugins in two ways:

### Single File

Use a single file in `lua/bsa/plugins` when the plugin is small or mostly shared.

Examples:

- `lua/bsa/plugins/noclip.lua`
- `lua/bsa/plugins/whitelist.lua`

Top-level files are loaded by filename prefix:

- `sv_*.lua` for server-only
- `cl_*.lua` for client-only
- `sh_*.lua` for shared
- no prefix defaults to shared

---

### Folder Plugin

Use a folder when the client and server parts are large enough to justify separate entry points.

Example:

```text
lua/bsa/plugins/logging/
  sv_init.lua
  cl_init.lua
```

Folder plugins load these entry files when present:

- `sv_init.lua`
- `cl_init.lua`
- `sh_init.lua`

---

## Typical Authoring Flow

1. Pick a stable plugin name. That name becomes the registration key, config key, sync key, and persistence filename.
2. Create the plugin table and fill in its metadata such as `description`, `config`, and optional `permissions`.
3. Implement `plugin:constructor()` for runtime setup.
4. Register Garry's Mod hooks with `self:add_hook(...)` instead of raw `hook.Add(...)`.
5. Clean up non-hook resources in `plugin:destructor()`.
6. Finish with `BSA.Plugins:add("<name>", plugin)`.

## Example

```lua
local plugin = {}
plugin.description = "Allows players with utility.noclip to noclip."
plugin.config = {
    alias = "Noclip",
    permissions = {"management.noclip"},
    sync = true
}
plugin.client_config = {
    alias = "Noclip",
    permissions = {"*"}
}
plugin.permissions = {
    "utility.noclip"
}

function plugin:constructor()
    self:add_hook("PlayerNoClip", self:id(), function(invoker, state)
        if BSA.Players.HasPermission(invoker, "utility.noclip") then
            return true
        end
    end)
end

function plugin:destructor()
end

BSA.Plugins:add("noclip", plugin)
```
