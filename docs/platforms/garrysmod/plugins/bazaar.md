# {{ state("private") }} {{ realm("shared") }} Bazaar
A fixed-price, bulk marketplace for mass buy/sell actions, built on the currency and inventory systems.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

!!! note
	This adds a dedicated table to BSA under `Bazaar` when enabled, and composes the `currency` and `inventory` plugins.\
	`BSA.Bazaar` is `nil` until the plugin is enabled, server methods fail with `subsystems_unavailable` if either dependency is missing.

## Functions
All server methods are asynchronous; the callback is optional unless noted.\
Mutating callbacks follow `callback(status: boolean, result_or_err)` where `result_or_err` is a short error string on failure.

### Listing & buying

- {{ realm("server") }} `#!ts bazaar:list(seller: Player | Steam, opts: table, callback: function(status: boolean, listing_id?: number))`\
	Creates a fixed-price listing.\
	The full listing tax is debited from the seller upfront and the stack is moved into escrow.\
	`opts`: `unit_price`, `currency_type`, either `item_id` (precise stack) or `item_type` (by type), optional `stack` quantity, and optional `scope`.

- {{ realm("server") }} `#!ts bazaar:massbuy(buyer: Player | Steam, item_type: string, currency_type: string, quantity: number, opts: table, callback: function(status: boolean, result?: table))`\
	Buys up to `quantity` units of `item_type` cheapest-first across all visible listings.\
	Pass `{}` for `opts`.\
	On success the result is `{requested, filled, spent, fills}`; `filled < requested` is a normal partial-fill outcome.\
	Buyers cannot purchase from their own listings.

- {{ realm("server") }} `#!ts bazaar:collect(seller: Player | Steam, listing_id: number, callback: function(status: boolean, err?: string))`\
	Sweeps all accrued proceeds from a listing into the seller's wallet.\
	A fully-sold listing is deleted once its proceeds are collected.

- {{ realm("server") }} `#!ts bazaar:reclaim(seller: Player | Steam, listing_id: number, callback: function(status: boolean, err?: string))`\
	Cancels a listing: returns remaining stock and any uncollected proceeds, and refunds the unsold portion of the tax (`unit_tax * quantity_remaining`).

### Reading

- {{ realm("server") }} `#!ts bazaar:browse(filter: table, callback: function(listings: table[]))`\
	Returns in-stock, scope-visible listings ordered cheapest-first.\
	`filter`: optional `item_type`, `currency_type`, `limit` (1–100, default 50), `offset`.

- {{ realm("server") }} `#!ts bazaar:get(listing_id: number, callback: function(listing: table | false))`\
	Returns a single listing's current state.

- {{ realm("server") }} `#!ts bazaar:my_listings(seller: Player | Steam, callback: function(listings: table[]))`\
	Returns all of a seller's listings, newest first.

- {{ realm("client") }} `#!ts bazaar:browse(filter?: table): boolean`\
	Requests a browse from the server (rate-limited).\
	Returns `false` if throttled.\
	Results arrive via the `BSA.Bazaar:browsed` hook.

- {{ realm("client") }} `#!ts bazaar:mine(): boolean`\
	Requests the local player's own listings.\
	Results arrive via the `BSA.Bazaar:mine` hook.

- {{ realm("client") }} `#!ts bazaar:listings(): table[]`\
	Returns the last received browse result from the local cache.

- {{ realm("client") }} `#!ts bazaar:own(): table[]`\
	Returns the last received own-listings result from the local cache.

## Item eligibility & tax
An item is listable only when `bazaarable` is set - checked on the instance attribute `attributes.bazaarable` first, then the item type's static `bazaarable`.\
Tax is charged at list time for the entire quantity and is instantly refundable for unsold units via `reclaim`, tax on sold units is non-refundable.

## Scopes
`opts.scope` controls where a listing is visible.\
Accepts `"community"` (everywhere), `"provider"` / `"service"` / `"server"` (the current one), a named form like `"server:name"`, a raw `{provider_id?, service_id?, server_id?}` tuple, or an array of these.\
Omit for community-wide.

## Hooks

- {{ realm("server") }} `BSA.Bazaar:changed` - fired after any mutation, and when another server's change arrives over Interlink. No arguments.
- {{ realm("client") }} `BSA.Bazaar:browsed(listings: table[])` - a browse result arrived.
- {{ realm("client") }} `BSA.Bazaar:mine(listings: table[])` - an own-listings result arrived.

## Example
Listing a stack and mass-buying from the marketplace.

```lua
-- server: list 64 of a player's stack at 10 credits each
local function list_stack(seller, item_id)
	local bazaar = BSA.Bazaar
	if not bazaar then return end

	bazaar:list(seller, {
		item_id = item_id,
		stack = 64,
		unit_price = 10,
		currency_type = "credits",
	}, function(ok, listing_id)
		if not ok then return seller:ChatPrint("List failed: " .. listing_id) end
		seller:ChatPrint("Listed as #" .. listing_id)
	end)
end

-- server: buy 20 units cheapest-first
local function buy_some(buyer)
	local bazaar = BSA.Bazaar
	if not bazaar then return end

	bazaar:massbuy(buyer, "credits_token", "credits", 20, {}, function(ok, result)
		if not ok then return buyer:ChatPrint("Buy failed: " .. result) end
		buyer:ChatPrint(("Bought %d/%d for %s"):format(result.filled, result.requested, result.spent))
	end)
end
```
