# {{ realm("server") }} Admission
A connection-time resolver that coalesces and caches punishment and group lookups so pre-connect enforcement (GeoBlock, bans) does not spam the database with duplicate queries.

!!! info
	See [core/database/tables/admission.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/database/tables/admission.lua) for the actual design implementation.

## Functions

- `#!ts admission:punishments(id64: string, callback: function(punishments))`\
	Looks up active punishments for a SteamID64. Delegates to `BSA.Storage.Punishments:lookup`.

- `#!ts admission:groups(id64: string | Player, callback: function(groups: table[] | false))`\
	Resolves a player's groups (primary plus secondaries) with a 20-second cache and in-flight request coalescing, concurrent calls for the same id share one query.\
	Calls `callback(false)` if Interlink is not alive or the account is unknown.

- `#!ts admission:invalidate(id64: string | Player)`\
	Evicts one player's cached group result.

- `#!ts admission:flush()`\
	Clears the entire group cache.

## Notes
The group cache invalidates itself when a player's membership changes (primary/secondary group updates) and flushes wholesale on any group or permission change, so callers normally never manage it manually.
