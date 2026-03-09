# Configurate
Hierarchical, class-driven configuration tree with runtime validation, import/export, exposure-safe snapshots, and change/event dispatching.

!!! warning
	Due to how configurate stores data of non-referenced configs, the size may increase from adding/removing configs.\
	You can clean them by calling `prune` which is for deleting the non-referenced configs, this will however delete that data forever.

## Functions

- `#!ts configurate:new(): configurate.object`\
Creates a configuration manager with built-in classes and event dispatchers.

## Manager Object
Root controller and root container for all configuration nodes.

- `#!ts configurate:get(...path: string): any`\
Finds a node by path and returns `node:get()`.

- `#!ts configurate:set(value: any, ...path: string): boolean, string?`\
Finds a node by path and calls `node:set(value)`.

- `#!ts configurate:find(...path: string | string[]): configurate.proxy?`\
Finds a node by path.

- `#!ts configurate:add(class: string, name: string, options?: table): configurate.proxy`\
Alias of proxy `:add(...)` on the manager root.

- `#!ts configurate:condition(cfg: configurate.proxy, old: any, new: any): boolean, string?`\
Global condition hook used by every `node:set(...)`. Default returns `true`.

- `#!ts configurate:flatten(children?: table, out?: configurate.proxy[]): configurate.proxy[]`\
Recursively collects child nodes.

- `#!ts configurate:export(): table`\
Returns shallow copy of manager `registry` (includes private/internal metadata).

- `#!ts configurate:expose(): table`\
Returns shallow copy of manager `exposure` (transport-safe metadata view).

- `#!ts configurate:import(data: table)`\
Imports child datasets into existing children by key.

- `#!ts configurate:prune(): number`\
Intended to prune stale nodes at root.

- `#!ts configurate:count(): number, number`\
Intended to count active/inactive nodes at root.

- `#!ts configurate:register(name: string, struct: table)`\
Registers a new configuration class inheriting from `configurate.proxy`.

## Manager Events
All are `dispatcher` instances. Callback returns are ignored.

- `#!ts configurate.added(parent: configurate.proxy | configurate.object, child: configurate.proxy)`
- `#!ts configurate.removed(node: configurate.proxy, absolute?: boolean)`
- `#!ts configurate.changed(node: configurate.proxy, old: any, new: any)`
- `#!ts configurate.imported(node: configurate.proxy)`
- `#!ts configurate.exported(node: configurate.proxy)`
- `#!ts configurate.exposed(node: configurate.proxy)`
- `#!ts configurate.pruned(node: configurate.proxy, removed_count: number)`

## Proxy Object
Each configuration entry is a `configurate.proxy` subclass instance.

- `#!ts node:add(class: string, name: string, options?: table): configurate.proxy`\
Creates/replaces a named child with the requested class.

- `#!ts node:remove(absolute?: boolean)`\
Removes this node from runtime tree.\
If `absolute == true`, also removes persisted `_c[name]` data from parent registry/exposure.

- `#!ts node:get(): any`\
Returns stored `_v`.

- `#!ts node:set(value: any): boolean, string?`\
Pipeline order: `validate -> override -> debounce -> node:condition -> manager:condition -> commit -> change/events`.

- `#!ts node:condition(old: any, new: any): boolean, string?`\
Per-node condition hook. Default returns `true`.

- `#!ts node:change(old: any, new: any)`\
Per-node side effect hook after commit. Default no-op.

- `#!ts node:override(old: any, new: any): any`\
Per-node mutation hook before debounce. Default returns `new`.

- `#!ts node:debounce(old: any, new: any): boolean, string?`\
Change gate. Default blocks identical non-table values.

- `#!ts node:validate(old: any, new: any): boolean, string?`\
Type/rule validator. Default returns `true`.

- `#!ts node:export(): table`\
Shallow copy of node `registry` + `_l` absolute path string.

- `#!ts node:expose(): table`\
Shallow copy of node `exposure` + `_l` absolute path string.

- `#!ts node:import(dataset: table, carry?: boolean): boolean, string?`\
Imports node value and child datasets.\
When `carry` is false, requires location match (`dataset._l == node:path(true)`).

- `#!ts node:prune(top_level?: configurate.proxy): number`\
Prunes inactive (`_r == false`) child data recursively and returns removed count.

- `#!ts node:count(): number, number`\
Returns recursive active/inactive child counts from registry data.

- `#!ts node:restore()`\
Base behavior clears `_v` in registry/exposure.\
Built-in typed classes override this to apply defaults through `set(...)`.

- `#!ts node:is(...path: string | string[] [, true]): boolean`\
Path comparison helper.\
If last arg is `true`, treats comparison as absolute path mode.

- `#!ts node:find(...path: string | string[]): configurate.proxy?`\
Finds descendant relative to this node.

- `#!ts node:path(concat?: boolean): string[] | string`\
Returns path segments, or dot-joined path when `concat == true`.

- `#!ts node:list(): configurate.proxy[]`\
Returns lineage list from top-level child down to this node.

- `#!ts node:flatten(children?: table, out?: configurate.proxy[]): configurate.proxy[]`\
Recursively collects descendants.

## Proxy Events
All are `dispatcher` instances. Callback returns are ignored.

- `#!ts node.added(listener_node: configurate.proxy, parent: configurate.proxy, child: configurate.proxy)`
- `#!ts node.removed(listener_node: configurate.proxy, removed_node: configurate.proxy, absolute?: boolean)`
- `#!ts node.changed(listener_node: configurate.proxy, changed_node: configurate.proxy, old: any, new: any)`
- `#!ts node.imported(node: configurate.proxy)`
- `#!ts node.exported(node: configurate.proxy)`
- `#!ts node.exposed(node: configurate.proxy)`
- `#!ts node.pruned(listener_node: configurate.proxy, pruned_node: configurate.proxy)`

## Built-In Classes
Registered in constructor via `configurate:register(type, struct)`.

- `#!ts container`\
Structure-only node. `set(...)` always fails with `"containers cannot contain values"`.

- `#!ts boolean`\
Value type: boolean. Default `options.default` or `false`.

- `#!ts number`\
Value type: number. Default `options.default` or `0`.\
Supports clamp via `options.min`/`options.max`.

- `#!ts string`\
Value type: string. Default `options.default` or `""`.\
Supports length bounds via `options.min`/`options.max`.

- `#!ts vector`\
Value type: `Vector`. Stored as table `{x,y,z}` internally; `get()` returns cached `Vector`.\
Supports per-axis clamp tables in `options.min`/`options.max`.

- `#!ts angle`\
Value type: `Angle`. Stored as table `{p,y,r}` internally; `get()` returns cached `Angle`.\
Supports per-axis clamp tables in `options.min`/`options.max`.

- `#!ts color`\
Value type: color-like table (`r,g,b[,a]`) or `Color`-style table.\
Channels are clamped to `0..255`; `a` defaults to `255`.

## Internal Dataset Fields
Serialized trees use these keys:

- `#!ts _n`: class/type name
- `#!ts _c`: children map
- `#!ts _v`: value payload
- `#!ts _o`: options (exposure side)
- `#!ts _r`: runtime-active marker (used for pruning)
- `#!ts _l`: absolute dot path (added by `export`/`expose`)
