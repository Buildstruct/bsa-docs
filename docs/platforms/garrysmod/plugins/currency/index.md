# {{ state("private") }} {{ realm("shared") }} Currency
A dynamic currency system utilizing NSS for arbitrary-precision & literal cookie clicker levels of crazyness.\
This currency system also specializes in keeping multi-sessions supported via cache invalidations.

!!! danger
    This plugin is private for buildstruct, therefore there is limited information about the inner workings of this system.

!!! warning
	Obviously this system can go way beyond the 64-bit integer limit, but its not always a good idea to go too far beyond as NSS does have some compute constrants in terms of processing speed.\
	A common example is `NSS:toString()`, which requires interative division to determine string representation of numbers in its entirety.

!!! note
	This adds a dedicated table to BSA under `Currency` when enabled.

## Functions

- `#!ts currency:register(name: string, alias: string, color: Color)`\
	Adds a new currency type, must be called shared.

- `#!ts currency:set(target: Player | Steam, type: string, value: nss.object | number | string, callback?: function(status: boolean))`\
	Sets the current amount of currency on a player.\
	Not providing a callback will assume an active player.

- `#!ts currency:get(target: Player | Steam, type: string, callback?: function(value?: nss.object)): nss.object`\
	Gets the current amount of currency on a player.\
	Not providing a callback will assume an active player.

- `#!ts currency:has(target: Player | Steam, type: string, value: nss.object | number | string, callback?: function(status: boolean, err?: string)): nss.object`\
	Gets the current amount of currency on a player.\
	Not providing a callback will assume an active player.

- `#!ts currency:add(target: Player | Steam, type: string, value: nss.object | number | string, callback?: function(status: boolean, err?: string))`\
	Adds to current amount of currency on a player.\
	Not providing a callback will assume an active player.

- `#!ts currency:afford(target: Player | Steam, type: string, cost: nss.object | number | string, callback: function(status: boolean, err?: string))`\
	Atomically safe afford check for if a player can make a purchase.

- {{ realm("server") }} `#!ts currency:spend(target: Player | Steam, type: string, cost: nss.object | number | string, callback: function(status: boolean, err?: string))`\
	Atomically safe afford with spending check for if a player is attempting to make a purchase.\
	This will attempt to deduct currency if they have any.

- {{ realm("server") }} `#!ts currency:escrow(target: Player | Steam, type: string, cost: nss.object | number | string, callback: function(status: boolean, escrow_id?: number | string))`\
	Atomic & guarded spending with a lifetime.\
	Upon server reboot these are refunded.

- {{ realm("server") }} `#!ts currency:refund(escrow_id: number, callback?: function(status: boolean, err?: string))`\
	Refunds an escrow that was generated.\
	This invalidates the escrow id.

- {{ realm("server") }} `#!ts currency:commit(escrow_id: number, callback?: function(status: boolean, err?: string))`\
	Commits an escrow that was generated.\
	This invalidates the escrow id.

- {{ realm("server") }} `#!ts currency:top(type: string, limit: number, callback: function(data: table[] | false, err?: string))`\
	Returns the top `limit` players by balance for the given currency type, ordered highest-first.\
	This does return tables of each player this function has found, similar to `bsa_players` but just their identifier and username, currency is stored under each as `sets`.

- {{ realm("server") }} `#!ts currency:inflation(type: string, callback: function(total: nss.object | false, err?: string))`\
	Returns an **estimated** total of the given currency type currently in circulation across all players.

## Example

This is an example of how you can integrate the currency system.

```lua
hook.Add("BSA.Plugins:enable", "Gears", function(name, plugin)
    if name ~= "currency" then return end
    plugin:register("gear", "Gear", Color(218,165,32))
end)

local PLAYER = FindMetaTable("Player")

if SERVER then
    function PLAYER:AddGears(value)
        local currency = BSA.Currency
        if not currency then return end
        currency:add(self, "gear", value)
    end

    function PLAYER:SetGears(value)
        local currency = BSA.Currency
        if not currency then return end
        currency:set(self, "gear", value)
    end

    function PLAYER:SpendGears(value, callback)
        local currency = BSA.Currency
        if not currency then return callback(false) end
        currency:spend(self, "gear", value, callback)
    end
end

function PLAYER:CanAffordGears(value, callback)
    local currency = BSA.Currency
    if not currency then return callback(false) end
    currency:afford(self, "gear", value, callback)
end

function PLAYER:GetGears()
    local currency = BSA.Currency
    if not currency then return BSA.NSS:new() end
    return currency:get(self, "gear")
end
```