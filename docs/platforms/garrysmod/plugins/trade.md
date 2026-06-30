# {{ state("private") }} {{ realm("server") }} Trade
An atomic, server-authoritative exchange of items and currency between players, built on the inventory and currency escrow systems.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

!!! note
	Trade is server-only and composes the `currency` and `inventory` plugins.\
	`BSA.Trade` is `nil` until the plugin is enabled, and every method fails with `subsystems_unavailable` if either dependency is missing, always guard before use.

## Bundle
Both methods operate on a **bundle** describing the items and/or currency to move.\
Both keys are optional, an empty bundle (`{}`) is a valid no-op side.

```lua
{
	-- numeric item ids -> integer quantity
	items = { [item_id] = quantity },
	-- currency type -> nss-coercible amount
	currency = { [currency_type] = amount },
}
```

Item ids must exist in the owner's inventory.\
Non-positive quantities and amounts are skipped.\
Currency amounts are coerced through `BSA.NSS.fromAny`, so numbers, strings, and NSS objects are all accepted.

## Functions

- `#!ts trade:trade(a: Player, b: Player, a_data: bundle, b_data: bundle, callback?: function(status: boolean, err?: string))`\
	Atomically swaps two bundles: `a` gives `a_data` to `b`, and `b` gives `b_data` to `a`.\
	Both bundles may only contain tradable items (see below).\
	If either side fails to escrow, everything already held is refunded before the callback fires.

- `#!ts trade:transfer(from: Player, to: Player, data: bundle, callback?: function(status: boolean, err?: string))`\
	One-way move of `data` from `from` to `to`.\
	Intended for admin and system-initiated moves — it bypasses the tradable check entirely.

Both methods are asynchronous.\
`callback(true)` means the exchange completed; `callback(false, err)` means it was aborted and all held escrows refunded.\
`err` is one of `subsystems_unavailable`, `owner_not_found`, `item_not_found`, `not_tradable` (trade only), or `escrow_failed`.

!!! warning
	Atomicity covers the escrow phase: if any hold fails, all prior holds are refunded.\
	Once both sides are fully held the merge is terminal and will not roll back, so ensure both players are valid and loaded before initiating.\
	Ephemeral escrows are also voided and refunded if the server restarts mid-exchange.

## Tradable items
`trade` only moves items flagged tradable.\
The flag resolves in priority order:

1. the item instance attribute `attributes.tradable`,
2. the item type's static `tradable`,
3. default `true`.

Set `tradable = false` on an instance or item type to block it from trades.\
`transfer` ignores this entirely.

## Example
A simple server-side gift command that hands one of the caller's item stacks to another player.

```lua
hook.Add("ExampleGift", "trade_gift", function(giver, receiver, item_id, amount)
	local trade = BSA.Trade
	if not trade then return end

	trade:trade(giver, receiver, {
		items = { [item_id] = amount }
	}, {}, function(ok, err)
		if not ok then
			giver:ChatPrint("Gift failed: " .. err)
			return
		end
		giver:ChatPrint("Gift sent.")
	end)
end)
```
