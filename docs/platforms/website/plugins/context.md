# Context Reference

`ctx` is the single surface injected into every plugin. All scoped resources registered through it are released automatically on disable.

## Lifecycle

- `constructor(ctx)` — sync registration only (config, routes, receivers). Must not `await`.
- `start()` — optional async; runs once DB + interlink are connected.
- `destructor()` — optional; only needed for things `ctx` cannot track (file handles, external state).

## ctx surface

- `ctx.name` · `ctx.descriptor` — plugin identity and parsed `plugin.json`.
- `ctx.logger(tag?)` — namespaced logger.
- `ctx.config` — `plugins.<name>` Configurate node. Build the schema in the constructor.
- `ctx.route` — scoped route registrar (`get`/`post`/`put`/`del`/`patch`). Routes are dropped on disable.
- `ctx.interlink`
    - `receive(cmd, cb)` — cross-server command handler (auto-unbound on disable).
    - `broadcast(cmd, ...args)` · `send(target, cmd, ...args)` · `omit(target, cmd, ...args)`
    - `server()` — this server's row once identity resolves.
    - `onConnected(fn)` — run now if connected, and on every reconnect.
- `ctx.ws` — `broadcast` · `broadcastAuthenticated` · `broadcastToPermission(permission, msg)`.
- `ctx.storage` — `Storage.Global` / `Storage.Local` datastores.
- `ctx.commands.invoked` — host bus fired when a command is invoked.
- `ctx.on(dispatcher, cb)` — subscribe to any host dispatcher; auto-disconnected on disable.
- `ctx.dispatcher<T>(name)` — create a plugin-owned event bus; destroyed on disable.
- `ctx.permissions.add(name, alias?)` · `ctx.permissions.has(account, name)` — register and check permissions.
- `ctx.interval(ms, fn)` · `ctx.timeout(ms, fn)` — tracked timers, cleared on disable.
- `ctx.onDisable(fn)` — extra teardown callback, run in reverse order on disable.

## Route gating

Routes registered with no options inherit the plugin's declared `permission`.\
Pass explicit options to override — `{}` for a public endpoint, or `{ permission }` for a narrower gate.

## Config persistence

Config is restored from `data/config/shared/plugins/<name>.json` before the constructor runs.\
Guard `ctx.config.add(...)` calls with `if (!ctx.config.find(...))` to avoid overwriting saved state.

## UI state persistence

Window state is round-tripped through the workspace autosave.

- B1: props `data` (restored on mount) and `setData(next)`.
- B2: the host assigns `element.data` and `element.setData(next)`.

Persist small JSON-serializable snapshots. Do not persist volatile state like scroll position.
