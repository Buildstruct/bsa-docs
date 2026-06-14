# {{ realm("shared") }} Flux
One network string wrapper for multi-channel messaging with SFB/SFS serialization, optional chunk streaming, and built-in replicated variables.

!!! info
	See [core/libraries/flux.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/flux.lua) for the actual design implementation.

!!! note
	Garry's Mod has two distinct modes of networking: Reliable & Unreliable.\
	We recommend using Unreliable for non-critical data, like log streaming for example.\
	Doing so relieves pressure on the reliable channel which is used way too often by others.

!!! note
	This adds a dedicated & constructed table to BSA as `Flux`.

## Functions

- `#!ts flux:new(tag: string): flux.object`\
	Creates a new flux manager bound to a single net tag (`util.AddNetworkString` on server).

## Object
These are returned from `flux:new(...)` or `__namecall`.

- {{ realm("server") }} `#!ts flux:isconnected(invoker: Player): boolean`\
	Checks if a player is considered fully connected by flux's internal start-command counter.

- {{ realm("server") }} `#!ts flux:stale()`\
	Cleans timed-out incoming/outgoing stream buckets using `stream_timeout`.

- `#!ts flux:identifier(name: string): number`\
	Returns CRC-based channel identifier (`tonumber(util.CRC(name))`).

- `#!ts flux:register(name: string): number`\
	Registers channel name <-> identifier mapping and returns the identifier.

- `#!ts flux:receive(name: string, callback?: function(buffer: flux.decoder, size: number, invoker?: Player))`\
	Registers or clears a channel callback.

- `#!ts flux:start(channel?: string, unreliable?: boolean): flux.encoder`\
	Constructs an encoder for writing and sending a payload.

## Runtime Events
These are `dispatcher` objects on each flux instance.\
Expected returns from these callbacks are ignored by `flux` internals.

- `#!ts flux.sending(encoder: flux.encoder, compressed: string, targets: Player[])`\
	Invoked before standard sends (`send`, `broadcast`, `omit`).

- {{ realm("server") }} `#!ts flux.pvsing(encoder: flux.encoder, compressed: string, ...: any)`\
	Invoked before `:pvs(...)`.

- {{ realm("server") }} `#!ts flux.pasing(encoder: flux.encoder, compressed: string, ...: any)`\
	Invoked before `:pas(...)`.

- `#!ts flux.receiving(buffer: flux.decoder, compressed: string)`\
	Invoked after successful decode.

- `#!ts flux.streaming(channel: string, stream_id: number, state: number, packet: string, invoker?: Player)`\
	Invoked on stream packets and acks.\
	`state`: `1` (stream chunk), `2` (stream end), `3` (stream ack).

- {{ realm("server") }} `#!ts flux.connected(invoker: Player)`\
	Invoked when a player transitions into connected state.

- {{ realm("server") }} `#!ts flux.disconnected(invoker: Player)`\
	Invoked when a connected player disconnects.

## Encoder
Constructed by `flux:start(...)`.\
Inherits low-level write methods from `sfb.Writer`.

- `#!ts flux.encoder:new(channel?: string, unreliable?: boolean): flux.encoder`\
	Creates an encoder instance (explicit constructor form).

- `#!ts flux.encoder:clone(): flux.encoder`\
	Creates a copy of the encoder with its current write stack, exclusions, inclusions, and streaming state.

- `#!ts flux.encoder:fork(): flux.encoder`\
	Creates a copy of the encoder's targeting configuration (exclusions, inclusions, streaming) without copying the write stack.

- `#!ts flux.encoder:merge(other: flux.encoder): self`\
	Appends another encoder's write stack onto this one.

- `#!ts flux.encoder:reset(): self`\
	Clears current write stack/buffer (also drops any compile cache).

- `#!ts flux.encoder:cachable(state?: boolean): self`\
	Toggles compile caching (default disabled, omitting `state` enables it).\
	Disabling drops any existing cache.

- `#!ts flux.encoder:cached(): boolean`\
	Returns whether caching is enabled and a compiled payload is currently cached.

- `#!ts flux.encoder:uncache(): self`\
	Drops the cached payload without disabling caching.

- `#!ts flux.encoder:compile(): string`\
	Returns the compressed payload (`util.Compress` of the encoded stack).\
	When caching is enabled, reuses the cached result until the write stack length changes.

- `#!ts flux.encoder:reliable(state: boolean): self`\
	Sets reliability mode (`true` = reliable, `false` = unreliable).

- `#!ts flux.encoder:isreliable(): boolean`\
	Returns reliability state.

- `#!ts flux.encoder:channel(channel: string): self`\
	Changes target channel and registers it.

- `#!ts flux.encoder:size(): number`\
	Returns encoded byte length before compression.

- `#!ts flux.encoder:table(value: table): self`\
	Encodes value through SFS, then writes length + data.

- `#!ts flux.encoder:any(value: any): self`\
	Encodes any value through SFS, then writes length + data.

- `#!ts flux.encoder:stream(state: boolean, capacity?: number): self`\
	Enables chunk streaming for large compressed payloads.\
	`capacity` must be >= `flux.stream_minsize`.

- `#!ts flux.encoder:stream_generate(): number`\
	Generates stream id.

- `#!ts flux.encoder:stream_status(player?: Player): number`\
	Returns stream progress from `0..1` (`1` when complete/unknown).

- {{ realm("server") }} `#!ts flux.encoder:exclude(...: Player): self`\
	Adds players to exclusion list (also removes them from inclusion list).

- {{ realm("server") }} `#!ts flux.encoder:include(...: Player): self`\
	Adds players to inclusion list (also removes them from exclusion list).

- {{ realm("server") }} `#!ts flux.encoder:pas(...): self`\
	Sends using `net.SendPAS(...)`.\
	Does not support streaming.

- {{ realm("server") }} `#!ts flux.encoder:pvs(...): self`\
	Sends using `net.SendPVS(...)`.\
	Does not support streaming.

- {{ realm("server") }} `#!ts flux.encoder:broadcast(): self`\
	Sends to all humans (with include/exclude adjustments).

- {{ realm("server") }} `#!ts flux.encoder:near(position: Vector | Entity, radius: number): self`\
	Sends to players within radius of position/entity center.

- `#!ts flux.encoder:send(...: Player | Player[]): self`\
	Primary send method.\
	Client sends to server via `net.SendToServer()`, server sends to selected players.

- {{ realm("server") }} `#!ts flux.encoder:omit(...: Player): self`\
	Sends to human players except the supplied players.

## Decoder
Produced internally on receive callbacks.\
Inherits read methods from `sfb.Reader`.

- `#!ts flux.decoder:new(name: string, id: number, data: string, max_size?: number): flux.decoder`\
	Creates decoder instance.

- `#!ts flux.decoder:clone(): flux.decoder`\
	Creates a copy of the decoder, preserving the current read position.

- `#!ts flux.decoder:size(): number`\
	Returns reader size metadata.

- `#!ts flux.decoder:reset(data: string, max_size?: number): self`\
	Resets decoder to a new payload.

- `#!ts flux.decoder:table(): any`\
	Reads SFS payload (length-prefixed).

- `#!ts flux.decoder:any(): any`\
	Reads SFS payload (length-prefixed).

## Variables
`flux.variables` is constructed as `flux.variables = flux.variables:new(flux)` and provides replicated state storage for globals/entities/players.\
For callback hooks below, return values are ignored unless explicitly stated otherwise.

- `#!ts flux.variables:register(name: string, class?: table): flux.variables.schema`\
	Registers a variable schema and optionally overrides schema methods/properties.

-  `#!ts flux.variables.to_index(entity?: Entity | Player | true): number`\
	Converts entity/player/global target to registry index.\
	Globals are `0`, players are negative `UserID`, entities use positive `EntIndex`.

- `#!ts flux.variables.from_index(index: number): Entity | Player | false`\
	Converts registry index back to runtime target.

- `#!ts flux.variables:get(entity: Entity | Player, name: string, fallback?: any): any`\
	Reads entity/player value.

- `#!ts flux.variables:get(name: string, fallback?: any): any`\
	Reads global value.

- `#!ts flux.variables:gettable(entity?: Entity | Player | true): table`\
	Returns registry table for a target, or the full registry if omitted.

- `#!ts flux.variables:onchange(name: string, callback: function(entity: Entity | Player | false, name: string, old: any, new: any))`\
	Binds named change callback.\
	Expected return: ignored.

- {{ realm("server") }} `#!ts flux.variables:onfilter(name: string, callback: function(): Player | Player[])`\
	Binds named replication filter callback used when no schema filter is set.\
	Expected return: `Player` or `Player[]` send targets.

- `#!ts flux.variables:onsync(name: string, callback: function(invoker: Player))`\
	Binds named sync callback.\
	Expected return: ignored.

- {{ realm("server") }} `#!ts flux.variables:set(entity: Entity | Player, name: string, value: any, force?: boolean)`\
	Server: updates and replicates value (staged by default, immediate when `force`).\
	Client: no-op.

- {{ realm("server") }} `#!ts flux.variables:set(name: string, value: any, force?: boolean)`\
	Server global overload.\
	Client: no-op.

- {{ realm("server") }} `#!ts flux.variables:sync(clients?: Player | Player[])`\
	Server: sends full registry snapshot (streamed).\
	Client: no-op.

- {{ realm("server") }} `#!ts flux.variables:erase(entity: Entity | Player)`\
	Server: removes entry and broadcasts erase notice.\
	Client: no-op.

## Variable Schema
Returned by `flux.variables:register(...)`.\
Return values are only consumed for `onread`, `ondebounce`, `oncondition`, and `onfilter`.

- {{ realm("server") }} `#!ts schema:onwrite(callback: function(buffer: flux.encoder, entity: Entity | Player | false, value: any))`\
	Overrides write behavior.\
	Expected return: ignored.

- {{ realm("client") }} `#!ts schema:onread(callback: function(buffer: flux.decoder, entity: Entity | Player | false): any)`\
	Overrides read behavior.\
	Expected return: decoded value.

- {{ realm("server") }} `#!ts schema:ondebounce(callback: function(entity: Entity | Player | false, old: any, new: any): boolean)`\
	Overrides debounce behavior (`true` blocks replication/write).\
	Expected return: `boolean`.

- {{ realm("server") }} `#!ts schema:oncondition(callback: function(entity: Entity | Player | false, value: any): boolean?)`\
	Optional server-side replication gate (`false` blocks replication).\
	Expected return: `false` to block, anything else to allow.

- {{ realm("server") }} `#!ts schema:onfilter(callback: function(entity: Entity | Player | false): Player | Player[])`\
	Optional per-schema target filter for replication.\
	Expected return: `Player` or `Player[]` send targets.

- `#!ts schema:onchange(callback: function(entity: Entity | Player | false, old: any, new: any))`\
	Runs when value changes locally.\
	Expected return: ignored.

- `#!ts schema:onsync(callback: function(entity: Entity | Player | false, value: any))`\
	Runs when sync/replication applies a value.\
	Expected return: ignored.
