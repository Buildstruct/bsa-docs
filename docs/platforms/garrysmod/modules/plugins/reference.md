# {{ realm("shared") }} Plugin Runtime Reference

For a practical authoring guide, see [Creating a Plugin](creating.md).

## Manager API

- `#!ts plugins:add(name: string, struct: table): plugin.class`\
  Registers a plugin definition, creates `config.Plugins.<name>`, and returns the registered plugin class.

- `#!ts plugins:enable(name: string): boolean, ...`\
  Enables a registered plugin if it is not already active.

- `#!ts plugins:disable(name: string): boolean, ...`\
  Disables an active plugin instance.

- `#!ts plugins:remove(name: string): boolean, ...`\
  Disables the plugin if needed and removes it from the registry.

- `#!ts plugins:get(name: string, active?: boolean): plugin.class | plugin.object | false`\
  Returns the registered plugin class.\
  Setting `active` to true will attempt to find the activated plugin thats running.

- `#!ts plugins:list(active?: boolean): (plugin.class | plugin.object)[]`\
  Returns the registry table.\
  Setting `active` to true will return a list of activated plugins.

## Base Plugin Methods

Every registered plugin inherits from the base `plugin` class.

- `#!ts plugin:constructor()`\
  Called when the plugin is enabled.

- `#!ts plugin:destructor()`\
  Called when the plugin is disabled.

- `#!ts plugin:active(): boolean`\
  Returns whether the plugin instance is active.

- `#!ts plugin:disable()`\
  Shortcut for `#!ts plugins:disable(self.name)`.

- `#!ts plugin:enable()`\
  Shortcut for `#!ts plugins:enable(self.name)`.

- `#!ts plugin:remove()`\
  Shortcut for `#!ts plugins:remove(self.name)`.

- `#!ts plugin:transport(): table`\
  Returns transport-safe plugin information.

### Dispatcher Tracking

- `#!ts plugin:create_dispatcher(name: string): dispatcher.object`\
  Creates a new dispatcher object.

- `#!ts plugin:add_dispatcher(handle: dispatcher, callback: function, id?: string): dispatcher.handle`\
  Connects a callback to a dispatcher and tracks the `dispatcher.handle` for automatic cleanup. Uses `<plugin>.<id>` as the identity.

- `#!ts plugin:remove_dispatcher(handle: dispatcher, id?: string): boolean`\
  Disconnects a tracked dispatcher handle.

- `#!ts plugin:clear_dispatchers()`\
  Disconnects all tracked dispatcher connections for the plugin instance.

### Hook Tracking

- `#!ts plugin:add_hook(name: string, id: string, callback: function)`\
  Adds a tracked hook using `<plugin>.<id>` as the final hook ID.

- `#!ts plugin:remove_hook(name: string, id: string)`\
  Removes one tracked hook.

- `#!ts plugin:clear_hooks()`\
  Removes all tracked hooks for the plugin instance.

### Timer Tracking

- `#!ts plugin:simple_timer(delay: number, callback: function)`\
  Creates a one-shot timer with an auto-generated identity. Automatically unregisters after firing.

- `#!ts plugin:add_timer(id: string, delay: number, reps: number, callback: function)`\
  Creates a tracked timer using `<plugin>.<id>` as the identity. Use `0` reps for infinite repetition.

- `#!ts plugin:exist_timer(id: string): boolean`\
  Returns whether a tracked timer exists.

- `#!ts plugin:toggle_timer(id: string): boolean`\
  Toggles a tracked timer between paused and running.

- `#!ts plugin:pause_timer(id: string): boolean`\
  Pauses a tracked timer.

- `#!ts plugin:unpause_timer(id: string): boolean`\
  Unpauses a tracked timer.

- `#!ts plugin:repsleft_timer(id: string): number`\
  Returns remaining repetitions for a tracked timer.

- `#!ts plugin:timeleft_timer(id: string): number`\
  Returns remaining time until the next tick of a tracked timer.

- `#!ts plugin:adjust_timer(id: string, delay: number, reps?: number, callback?: function)`\
  Adjusts the delay, repetitions, or callback of an existing tracked timer.

- `#!ts plugin:stop_timer(id: string)`\
  Stops a tracked timer.

- `#!ts plugin:start_timer(id: string)`\
  Starts a stopped tracked timer.

- `#!ts plugin:remove_timer(id: string)`\
  Removes a tracked timer. Also aliased as `destroy_timer`.

- `#!ts plugin:clear_timers()`\
  Removes all tracked timers for the plugin instance.

!!! note
    `create_timer` is an alias for `add_timer`.\
    `destroy_timer` is an alias for `remove_timer`.

### HTTP Tracking

- `#!ts plugin:http(url: string, callback: function, options?: table): request`\
  Performs an HTTP request with automatic retry support.\
  Returns a request handle that can be cancelled.\
  The callback receives `(code, body, headers)` on success or `(false, reason)` on failure.\
  Requests are automatically ignored if the plugin becomes inactive.

    **Options table:**

    | Field        | Type     | Default | Description                    |
    |-------------|----------|---------|--------------------------------|
    | `retry`     | `number` | `1`     | Number of retry attempts       |
    | `method`    | `string` | `"GET"` | HTTP method                    |
    | `body`      | `string` | `nil`   | Request body                   |
    | `type`      | `string` | `nil`   | Content type                   |
    | `timeout`   | `number` | `nil`   | Request timeout                |
    | `headers`   | `table`  | `{}`    | Request headers                |
    | `parameters`| `table`  | `{}`    | URL query parameters           |

- `#!ts plugin:cancel_http(request: table)`\
  Cancels a tracked HTTP request so its callback will not fire.

- `#!ts plugin:clear_https()`\
  Cancels all tracked HTTP requests for the plugin instance.

### Cleanup

- `#!ts plugin:clean()`\
  Runs full cleanup: clears tracked dispatchers, hooks, timers, and HTTP requests.

## Loader Behavior

The loader resolves the plugin directory relative to `plugins.lua` and then auto-includes plugin entry files.

### Top-Level Files

Files in `lua/bsa/plugins` are loaded by prefix:

- `sv_*` via `BSA.sv(...)`
- `cl_*` via `BSA.cl(...)`
- `sh_*` via `BSA.sh(...)`
- no prefix also via `BSA.sh(...)`

### Folder Plugins

For each subfolder in `lua/bsa/plugins`, the loader looks for:

- `sv_init.lua`
- `cl_init.lua`
- `sh_init.lua`

This is the pattern used by `logging`.

## Enable Sequence

When `plugins:enable(name)` succeeds, the runtime does this:

1. Looks up the registered plugin class.
2. Clears any previous failure state.
3. Creates a fresh plugin instance through the class `static` path.
4. Registers `plugin.permissions` into `BSA.Storage.Permissions` when interlink is alive.
5. Creates `config.Client.Plugins.<name>` on the client from `plugin.client_config`.
6. Creates `config.Language.Plugins.<name>` and attaches helper methods like `:phrase(...)`.
7. Runs `plugin:constructor()`.
8. Mounts `plugin.interface` on the client through `BSA.Interface:add(...)`.
9. Marks the plugin active, updates `config.Plugins.<name>`, and syncs the active list.
10. Invokes `plugins.enabled(plugin, true)`.

Failure behavior:

- Constructor/runtime errors are captured and stored in `plugin.failure`.
- If `constructor()` returns `false`, enable halts and `plugins.enabled(plugin, false, err)` is fired.

## Disable Sequence

When `plugins:disable(name)` runs, the runtime:

1. Calls `plugin:destructor()`.
2. Calls `plugin:clean()` which clears tracked dispatchers, hooks, timers, and HTTP requests.
3. Removes the client interface if one was mounted.
4. Removes the runtime client/language config containers for that plugin.
5. Removes dynamic child nodes created under `self.config`.
6. Clears the active registry entries.
7. Syncs the new active plugin list.
8. Invokes `plugins.disabled(plugin, state, err)`.

## Runtime Events

These dispatchers live on `plugins`:

- `#!ts plugins.synced()`  
  Client-side event fired after the replicated active-plugin list has been applied.

- `#!ts plugins.enabled(plugin: plugin.class, state: boolean, err?: string)`  
  Fired after an enable attempt. `state` is `true` on success.

- `#!ts plugins.disabled(plugin: plugin.class, state: boolean, err?: string)`  
  Fired after a disable attempt. `state` reflects whether `destructor()` completed without error.

### Hooks
This allows other addons to conveniently attach to plugins without the need of dispatcher dependency.

- `#!ts BSA.Plugins:enable(name: string, instance: plugin.object)`\
  Called upon a plugin being enabled.

- `#!ts BSA.Plugins:disable(name: string, instance: plugin.object)`\
  Called upon a plugin being disabled.

## Sync Behavior

- The server stores active plugin names in the replicated variable `bsa_plugins`.
- Clients enable any missing active plugins after receiving that variable.
- Runtime enable/disable deltas are also sent with:
  - `plugins.enable`
  - `plugins.disable`

In practice this means the server is authoritative for which plugins are active.

## Configuration And Persistence

Each plugin gets a top-level toggle under:

```text
config.Plugins.<name>
```

Server-side plugin config is persisted to:

```text
data/bsa/config/plugins/<name>.dat
```

Persistence behavior:

- Existing plugin config files are imported on startup.
- Changes and prunes under `config.Plugins` are saved back out through SFS.
- If the changed top-level config has `options.sync`, the global config sync path is triggered.

Because config is persisted by path, recreating the same child config names on the next enable restores the previous values.