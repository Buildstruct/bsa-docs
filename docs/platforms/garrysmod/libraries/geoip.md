# {{ realm("server") }} GeoIP
Resolves IP addresses to ISP, AS, and organization strings via external APIs with database-backed caching.

!!! info
	See [core/libraries/geoip.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/geoip.lua) and [core/modules/geoip.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/modules/geoip.lua) for the actual design implementation.

!!! note
	This adds a dedicated & constructed table to BSA as `GeoIP`.

## Functions

- `#!ts geoip:lookup(address: string, callback: function(geo|false, err?: string))`\
	Resolves a full address string (`ip:port` format accepted) to a geo result.\
	Checks `bsa_geoip` first, falls back to external APIs when no entry exists or the cached entry is older than one month.\
	Returns `{ip, isp, as, org}` on success.\
	Returns `false` and an error string on failure or private address.

- `#!ts geoip:isprivate(ip: string): string|false`\
	Returns a message string if the IP is in a known private range, `false` otherwise.

- `#!ts geoip:getdata(ip: string, callback: function(data|false, err?: string))`\
	Fetches raw geolocation data from external services, bypassing the database cache.

- `#!ts geoip:getplayerdata(player: Player, callback: function(data|false, err?: string))`\
	Convenience wrapper that reads `player:IPAddress()` and calls `getdata`.

- `#!ts geoip:request(ip: string, callback: function(data|false, err?: string))`\
	Low-level fallback chain that tries each configured service in order.\
	Accumulates error strings and only calls `callback(false, errors)` after all services are exhausted.
