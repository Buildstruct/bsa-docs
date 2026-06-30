# {{ state("private") }} {{ realm("shared") }} Inventory
A server-authoritative item storage system with custom item attributes, world drops, an audit ledger, and scope-based inventories that can range from a single server to community-wide across platforms.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

!!! note
	This adds a dedicated table to BSA under `Inventory` when enabled.\
	`BSA.Inventory` is the live plugin instance on both realms and is `nil` until the plugin loads, always guard before use.

## Registering item types
Item types are registered from the `BSA.Plugins:enable` hook, which fires on both realms so the registry is identical client and server.\
This is the only supported place to call `register`.

- `#!ts inventory:register(id: string, item: table): table`\
	Registers a new item type and returns the normalized definition.\
	`id` is a unique identifier.

The `item` table accepts:

| Field | Type | Default | Description |
|---|---|---|---|
| `name` | `string?` | prettified `id` | Display label. |
| `stackable` | `boolean?` | `true` | When `true`, plain (attributeless) instances of the same type and scope merge into one stack. When `false`, every instance is unique and must be targeted by `item_id`. |
| `static` | `table?` | `{}` | Community-wide metadata. Convention keys: `rarity` (number), `auctionable`, `bazaarable`, `tradable` (booleans). |
| `entity` | `string \| table?` | `nil` | Drop descriptor. `nil` = not droppable; a string names a scripted entity class; a `{model, scale?, material?}` table uses the built-in `bsa_inventory_drop` entity. |
| `OnGiven` | `function?` | — | {{ realm("server") }} Fired when an online player receives a stack: `function(ply, item_id, info: {source, stack})`. |
| `OnDestroyed` | `function?` | — | {{ realm("server") }} Fired when an online player's stack is fully consumed: `function(ply, item_id, info: {source, stack})`. |

```lua
hook.Add("BSA.Plugins:enable", "MyPlugin.Items", function(name, plugin)
	if name ~= "inventory" then return end
	plugin:register("soda_can", {
		name = "Soda Can",
		static = { rarity = 1, tradable = true },
		entity = { model = "models/props_junk/popcan01a.mdl" },
		OnGiven = function(ply, item_id, info) end,
	})
end)
```

- `#!ts inventory:display_name(item_type: string): string`\
	Returns the registered display name, or a prettified id for unknown types.\
	Available on both realms.

## Scope & stacking
Every stack carries a **scope** controlling which servers can see it.\
A `nil` or `"community"` scope is visible everywhere.\
Other forms: `"provider"` / `"service"` / `"server"` (the current one), a named form like `"server:name"`, a raw `{provider_id?, service_id?, server_id?}` tuple, or an array of these.

Whether two stacks of the same type collapse into one is driven automatically by their identity - owner, type, scope, and attributes:

- A **stackable** type with no per-instance `attributes` is fungible: repeated gives for the same owner, type, and scope merge into one stack.
- A **stackable** type **with** `attributes` merges only with stacks whose attributes are identical, attribute values are folded into the stack identity, so `{rarity=2}` and `{rarity=3}` stay separate while two `{rarity=2}` stacks combine.
- A **non-stackable** type never merges, every instance is a unique row that must be targeted by `item_id`.

Plugins never manage stack keys directly.\
Attributed *stackable* stacks can be located by `(scope, attributes)` like fungible ones, `item_id` is only mandatory for non-stackable types.

!!! note
	Identical-attribute merging applies to stacks created after this behavior shipped.\
	Attributed stacks created earlier hold a one-off identity and won't retro-merge with new gives.

## Cross-platform stacking
The same inventory can run on any platform that shares the database (Garry's Mod, Minecraft, the website, etc).\
The database itself never conflicts.\
But for two platforms to **merge the same stack**, three things must line up: the first is a standard this system guarantees, the other two are the developer's responsibility.

A stack's identity is `owner + item_type + scope + attributes`, reduced to a single `stack_key`.\
The attribute part is serialized with a fixed, language-neutral grammar so every platform produces a **byte-identical** key for equal attributes.\
If a port diverges, equal items simply stop merging across platforms, never an error.\
Keep this identical everywhere:

| Value | Encoding |
|---|---|
| nil | `z` |
| boolean | `b1` / `b0` |
| integer | `i<len>:<digits>` |
| float | `f<len>:<digits>` |
| string | `s<bytelen>:<raw bytes>` |
| array | `a<count>:` then each element |
| map | `m<count>:` then key/value pairs, keys sorted by their encoded bytes |

Everything is length-prefixed, so there are no escaping rules to disagree on.\
For example `{ rarity = 2, bound = true }` becomes `m2:s5:boundb1s6:rarityi1:2`. Use integers and strings for identity-bearing attributes, non-integer floats are best-effort only.

!!! danger "Gold standard"
	This serialization is a maintained cross-platform contract.\
	Changing it changes every `stack_key`, so any port must reproduce it exactly.

The two developer responsibilities:

- Register each shared `item_type` with the **same** `stackable` flag and attribute conventions on every platform, these live in code, not the database.
- Use the same write discipline (the optimistic `updated_at` guard and the escrow flow). The database blocks duplicate rows regardless, but skipping the guard can lose a concurrent update.

## Server methods
All server methods are asynchronous and DB-backed, results arrive in the optional `callback`.\
The `options` table shares these common fields where relevant: `stack` (quantity, default 1), `item_id` (target a specific stack), `scope`, `attributes` (per-instance JSON data), `source` (provenance label for the audit ledger), and `actor` (who initiated it, a `Player` or SteamID64).

- {{ realm("server") }} `#!ts inventory:give(target: Player | Steam, id: string, options: table, callback?: function(ok: boolean, item_id?: number))`\
	Gives `options.stack` of type `id` to `target`.\
	Stackable items merge with an existing stack of the same scope and attributes; non-stackable items always create a new stack.

- {{ realm("server") }} `#!ts inventory:take(target: Player | Steam, id: string, options: table, callback?: function(ok: boolean, remaining?: number))`\
	Removes items from `target`.\
	For stackable items `options.scope` (and `options.attributes`, if the stack was given with any) must match how they were given; for non-stackable items `options.item_id` is required.\
	`remaining` is the new quantity, or `nil` if the stack was emptied.

- {{ realm("server") }} `#!ts inventory:transfer(from: Player | Steam, to: Player | Steam, id: string, options: table, callback?: function(ok: boolean, item_id?: number))`\
	Atomically moves a stack from `from` to `to` in a single transaction; the recipient inherits the source scope and attributes.

- {{ realm("server") }} `#!ts inventory:rescope(item_id: number, scope, options: table, callback?: function(ok: boolean, surviving_item_id?: number))`\
	Changes a stack's scope.\
	A stackable item merges into an existing stack at the new scope if one exists; the callback returns the surviving stack id.

- {{ realm("server") }} `#!ts inventory:get(target: Player | Steam, callback: function(stacks: table[] | false))`\
	Fetches all stacks visible to this server for `target` (online or offline).\
	Each stack is `{item_id, item_type, quantity, attributes?}`.

- {{ realm("server") }} `#!ts inventory:count(target: Player | Steam, item_type: string, callback: function(total: number))`\
	Total quantity of `item_type` held across all visible stacks.\
	`0` if none.

- {{ realm("server") }} `#!ts inventory:has(target: Player | Steam, item_type: string, amount?: number, callback: function(has: boolean))`\
	Whether `target` holds at least `amount` (default 1).\
	`amount` may be omitted.

- {{ realm("server") }} `#!ts inventory:reveal(viewer: Player, target: Player | Steam, callback?: function(ok: boolean, items?: table[]))`\
	Pushes a one-off snapshot of `target`'s inventory to `viewer`, firing the client `BSA.Inventory:revealed` hook.

### Escrow
Escrow detaches a stack into a suspended hold that must later be resolved with `merge`, `commit`, or `refund`.\
Pass `options.durable = true` to make the hold survive a server restart (used by trade, auction, and bazaar); non-durable holds are auto-refunded on boot.

- {{ realm("server") }} `#!ts inventory:escrow(target: Player | Steam, id: string, options: table, callback?: function(ok: boolean, escrow_id?: number))`\
	Removes a stack from `target`'s inventory into a hold and returns the `escrow_id`.

- {{ realm("server") }} `#!ts inventory:merge(escrow_id: number, target: Player | Steam, options: table, callback?: function(ok: boolean, item_id?: number))`\
	Transfers the held stack to `target`.\
	`options.quantity` claims only part of the hold, leaving the rest in escrow.

- {{ realm("server") }} `#!ts inventory:commit(escrow_id: number, options: table, callback?: function(ok: boolean))`\
	Destroys the held stack permanently (consumed).

- {{ realm("server") }} `#!ts inventory:refund(escrow_id: number, options?: table, callback?: function(ok: boolean))`\
	Returns the held stack to its original owner.\
	`options.quantity` refunds only part.

### World drops
Drops require the item type to have been registered with an `entity` descriptor.

- {{ realm("server") }} `#!ts inventory:drop(target: Player | Steam, id: string, options: table, callback?: function(ok: boolean, escrow_id?: number, entity?: Entity))`\
	Escrows a stack from `target` and spawns a world entity at their aim.\
	Another player pressing USE commits it to themselves; the escrow auto-refunds if the server restarts before pickup.

- {{ realm("server") }} `#!ts inventory:spawn(id: string, options: table, callback?: function(ok: boolean, entity?: Entity)): Entity`\
	Spawns an ownerless world item (no escrow).\
	Pickup grants the picker a fresh stack.\
	`options` may include `attributes`, `pos`, and `ang`.

- {{ realm("server") }} `#!ts inventory:pickup(escrow_id: number, picker: Player | Steam, options: table, callback?: function(ok: boolean, item_id?: number))`\
	Commits an escrowed drop to `picker`.\
	Called automatically by the built-in USE handler; only call it manually for custom pickup flows.

## Client methods
The client holds a read-only cache of the local player's own inventory, kept in sync by server pushes.\
All client methods are synchronous.

- {{ realm("client") }} `#!ts inventory:get(item_id?: number): table | table[]`\
	One cached stack by id, or all cached stacks if no id is given.

- {{ realm("client") }} `#!ts inventory:count(item_type: string): number`\
	Total cached quantity of `item_type`.

- {{ realm("client") }} `#!ts inventory:has(item_type: string, amount?: number): boolean`\
	Whether the cache holds at least `amount` (default 1).

- {{ realm("client") }} `#!ts inventory:type(id: string): table | nil`\
	The registered type definition for `id`.

- {{ realm("client") }} `#!ts inventory:display_name(item_type: string): string`\
	Display name for `item_type`.

- {{ realm("client") }} `#!ts inventory:resync(): boolean`\
	Requests a full resync from the server.\
	Rate-limited; returns `false` if on cooldown.

- {{ realm("client") }} `#!ts inventory:viewing(identifier: string): table[] | nil`\
	The last reveal snapshot received for a SteamID64, or `nil`.

- {{ realm("client") }} `#!ts inventory:clear_viewing(identifier?: string)`\
	Clears the cached reveal for a player, or all reveals if no id is given.

## Hooks

- {{ realm("client") }} `BSA.Inventory:changed(item_id?: number, item?: table)`\
	The local cache changed.\
	On a full sync both arguments are `nil`; on an incremental delta both are set, and `item` is `nil` when the stack was removed.\
	Also available as the dispatcher `BSA.Inventory.changed`.

- {{ realm("client") }} `BSA.Inventory:revealed(identifier: string, items: table[])`\
	A reveal snapshot for `identifier` arrived.\
	Also available as the dispatcher `BSA.Inventory.revealed`.

## Example
Granting an item and reacting to client-side inventory changes.

```lua
-- server: grant 5 soda cans, scoped to this server only
if SERVER then
	local function reward(ply)
		local inv = BSA.Inventory
		if not inv then return end
		inv:give(ply, "soda_can", { stack = 5, scope = "server", source = "reward" })
	end
end

-- client: refresh a HUD whenever the local inventory changes
if CLIENT then
	hook.Add("BSA.Inventory:changed", "RefreshInventoryHUD", function(item_id, item)
		local inv = BSA.Inventory
		if not inv then return end
		-- rebuild from inv:get()
	end)
end
```
