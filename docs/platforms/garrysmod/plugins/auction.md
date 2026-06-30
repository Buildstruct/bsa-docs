# {{ state("private") }} {{ realm("shared") }} Auction
A player & automated marketplace for timed auctions and Buy-It-Now (BIN) listings, built on the currency and inventory systems.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

!!! note
	This adds a dedicated table to BSA under `Auction` when enabled, and composes the `currency` and `inventory` plugins.\
	`BSA.Auction` is `nil` until the plugin is enabled, server methods fail with `subsystems_unavailable` if either dependency is missing.

## Functions
All server methods are asynchronous, the callback is optional unless noted.\
Mutating callbacks follow `callback(status: boolean, result_or_err)` where `result_or_err` is a short error string on failure.

### Listing & settlement

- {{ realm("server") }} `#!ts auction:list(seller: Player | Steam, opts: table, callback?: function(status: boolean, listing_id?: number))`\
	Lists an item for `auction` or `bin`.\
	The listing tax is debited from the seller upfront and the item is moved into escrow.\
	`opts`: `listing_type`, `price`, `currency_type`, `duration` (seconds, required for auctions), and either `item_id` (precise stack) or `item_type` (by type) with optional `stack` quantity and `scope`.

- {{ realm("server") }} `#!ts auction:bid(bidder: Player | Steam, listing_id: number, amount: nss.object | number | string, callback?: function(status: boolean, err?: string))`\
	Places a bid on an active auction.\
	Must meet the ask price or the current high bid plus `min_increment`.\
	The previous high bidder's escrow is refunded immediately on outbid.

- {{ realm("server") }} `#!ts auction:buy(buyer: Player | Steam, listing_id: number, callback?: function(status: boolean, err?: string))`\
	Purchases a BIN listing outright.

- {{ realm("server") }} `#!ts auction:collect(player: Player | Steam, listing_id: number, callback?: function(status: boolean, what?: "item" | "payment"))`\
	Claims the buyer's won item or the seller's payment from a settled listing.\
	The role is resolved automatically from the listing.\
	The row self-destructs once both legs are collected.

- {{ realm("server") }} `#!ts auction:reclaim(seller: Player | Steam, listing_id: number, callback?: function(status: boolean, err?: string))`\
	Returns an unsold or no-bid listing's item to the seller and refunds the tax.

- {{ realm("server") }} `#!ts auction:reclaim_as_admin(listing_id: number, callback?: function(status: boolean, err?: string))`\
	Admin variant of `reclaim` that resolves the seller from the listing row without an identity check.

### Reading

- {{ realm("server") }} `#!ts auction:browse(filter: table, callback: function(listings: table[]))`\
	Returns active, scope-visible listings for this server.\
	`filter`: optional `item_type`, `currency_type`, `listing_type`, `limit` (1–100, default 50), `offset`.

- {{ realm("server") }} `#!ts auction:get(listing_id: number, callback: function(listing: table | false))`\
	Returns a single listing regardless of state.

- {{ realm("server") }} `#!ts auction:my_listings(seller: Player | Steam, callback: function(listings: table[]))`\
	Returns all of a seller's listings across every state, newest first.

- {{ realm("client") }} `#!ts auction:browse(filter?: table): boolean`\
	Requests a browse from the server (rate-limited).\
	Returns `false` if throttled.\
	Results arrive via the `BSA.Auction:browsed` hook.

- {{ realm("client") }} `#!ts auction:mine(): boolean`\
	Requests the local player's own listings.\
	Results arrive via the `BSA.Auction:mine` hook.

- {{ realm("client") }} `#!ts auction:listings(): table[]`\
	Returns the last received browse result from the local cache.

- {{ realm("client") }} `#!ts auction:own(): table[]`\
	Returns the last received own-listings result from the local cache.

## Item eligibility & tax
An item is listable only when `auctionable` is set - checked on the instance attribute `attributes.auctionable` first, then the item type's static `auctionable`.\
The listing tax is `floor(price * tax_bps / 10000)`, debited at list time and refunded on `reclaim`.

## Scopes
`opts.scope` controls where a listing is visible.\
Accepts `"community"` (everywhere), `"provider"` / `"service"` / `"server"` (the current one), a named form like `"server:name"`, a raw `{provider_id?, service_id?, server_id?}` tuple, or an array of these.\
Omit for community-wide.

## Hooks

- {{ realm("server") }} `BSA.Auction:changed` - fired after any mutation, and when another server's change arrives over Interlink. No arguments.
- {{ realm("client") }} `BSA.Auction:browsed(listings: table[])` - a browse result arrived.
- {{ realm("client") }} `BSA.Auction:mine(listings: table[])` - an own-listings result arrived.

## Example
Listing an item and reacting to marketplace changes.

```lua
-- server: list a player's stack as a 1-hour auction starting at 100 credits
local function list_item(seller, item_id)
	local auction = BSA.Auction
	if not auction then return end

	auction:list(seller, {
		listing_type = "auction",
		item_id = item_id,
		price = 100,
		currency_type = "credits",
		duration = 3600,
	}, function(ok, listing_id)
		if not ok then return seller:ChatPrint("List failed: " .. listing_id) end
		seller:ChatPrint("Listed as #" .. listing_id)
	end)
end

-- client: refresh a UI whenever the marketplace changes
hook.Add("BSA.Auction:changed", "RefreshAuctionUI", function()
	if not BSA.Auction then return end
	BSA.Auction:browse()
end)

hook.Add("BSA.Auction:browsed", "PopulateAuctionUI", function(listings)
	-- rebuild the listing panel from `listings`
end)
```
