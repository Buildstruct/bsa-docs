# Plugins
Plugin manager for registering, enabling, disabling, syncing, and unloading BSA plugins with lifecycle callbacks and hook cleanup.

## Functions

- `#!ts plugins:add(name: string, struct: table): plugin.class`\
Registers a plugin definition, creates `config.Plugins.<name>` (default `false`), and returns the registered plugin class.

## Manager Object

- `#!ts plugins:enable(name: string): boolean, ...`\
Enables plugin if registered and inactive. Runs static/class bootstrap, constructor, language/client config setup, permission registration, and sync broadcast.

- `#!ts plugins:disable(name: string): boolean, ...`\
Disables active plugin. Runs destructor, cleanup, config subtree cleanup, and sync broadcast.

- `#!ts plugins:remove(name: string): boolean, ...`\
Disables plugin (if needed) and removes it from registry.

- `#!ts plugins:get(name: string): plugin.class | false`\
Returns registered plugin class by name.

- `#!ts plugins:list(): table`\
Returns plugin registry table.

## Plugin Object
Base class is `plugin` (`plugins.class`). Individual plugins inherit from it.

- `#!ts plugin:constructor()`\
Lifecycle callback on enable.

- `#!ts plugin:destructor()`\
Lifecycle callback on disable.

- `#!ts plugin:active(): boolean`\
Returns whether plugin instance is currently active.

- `#!ts plugin:disable()`\
Shortcut for `plugins:disable(self.name)`.

- `#!ts plugin:enable()`\
Shortcut for `plugins:enable(self.name)`.

- `#!ts plugin:remove()`\
Shortcut for `plugins:remove(self.name)`.

- `#!ts plugin:transport(): table`\
Returns transport-safe plugin info: `name`, `alias`, `config` path, `description`, `permissions`, `active`, `failure`.

- `#!ts plugin:add_hook(name: string, id: string, callback: function)`\
Registers tracked hook under identity `<plugin>.<id>`.

- `#!ts plugin:remove_hook(name: string, id: string, callback?: function)`\
Removes one tracked hook.

- `#!ts plugin:clear_hooks()`\
Removes all tracked hooks owned by plugin.

- `#!ts plugin:clean()`\
Runs plugin cleanup routine (currently hook cleanup).

## Runtime Events
These are `dispatcher` objects on `plugins`. Return values are ignored.

- `#!ts plugins.synced()`\
Client-side event fired after replicated active-plugin list has been applied.

- `#!ts plugins.enabled(plugin: plugin.class, state: boolean, err?: string)`\
Fired after enable attempt. `state=true` on success, `false` on failure.

- `#!ts plugins.disabled(plugin: plugin.class, state: boolean, err?: string)`\
Fired after disable attempt. `state` reflects destructor success.

## Sync Behavior

- Server stores active plugin names in replicated variable `bsa_plugins`.
- Client receives this list and enables any missing active plugins, then invokes `plugins.synced`.
- Additional runtime deltas are sent with network channels:
    - `plugins.enable`
    - `plugins.disable`

## Loading Behavior

- Auto-loads plugin Lua files from `../../plugins` using prefix convention:
    - `sv_*` -> server include (`BSA.sv`)
    - `cl_*` -> client include (`BSA.cl`)
    - `sh_*` or no prefix -> shared include (`BSA.sh`)
- Also loads folder-based plugin entry files:
    - `sv_init.lua`
    - `cl_init.lua`
    - `sh_init.lua`

## Configuration and Persistence
Server-side plugin config under `config.Plugins` is persisted to:

- `data/bsa/config/plugins/<plugin>.dat`

Behavior:

- Existing plugin config files are loaded on startup (SFS decode + import).
- On `config.Plugins.changed` and `config.Plugins.pruned`, plugin configs are re-encoded and saved.
- If a changed top-level config has `options.sync`, global config sync is triggered.

## Notes

- Enable flow supports plugin halting by returning `false` from constructor path (`state=false` with error message).
- Failures during enable are captured in `plugin.failure` and exposed in `plugin:transport()`.
- Client plugin interfaces are mounted through `BSA.Interface:add(name, interface)` when provided.
