# {{ realm("shared") }} Repr
Structured colored text representation system used by BSA for readable value formatting, console/chat/interface output, and networked message delivery.

!!! info
	See [core/libraries/repr.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/repr.lua) and [core/modules/repr.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/modules/repr.lua) for the actual design implementation.

`repr` is defined in two layers:

- `libraries/repr.lua`: value conversion, serialization, and construction of `Color`/`string` expression arrays.
- `modules/repr.lua`: BSA-facing message builder class (`console/chat/interface/custom`) with transport helpers.

## Library API
These functions come from `libraries/repr.lua` and are available on `BSA.Repr`.

- `#!ts repr.typeof(value: any): string`\
    Extended type resolver (`Color`, `Entity`, `Player`, etc.).

- `#!ts repr.tostring(value: any, is_compact?: boolean): (table, boolean?)`\
    Converts a value into a colored expression chunk list.\
    Optional second return marks comma override behavior used by table serializer.

- `#!ts repr.tostring_concat(value: any, is_compact?: boolean): string`\
    String-only flatten of `repr.tostring` output (drops colors).

- `#!ts repr.stringify(tbl: table, spaces?: number, done?: table, construct?: table): table`\
    Builds a colored pretty-print representation of a table (recursive with depth/entry guards).

- `#!ts repr.serialize(tbl: table): boolean, table | string`\
    Safe table serialization wrapper around `stringify` (`pcall` protected).

- `#!ts repr.construct(entries: table): table`\
    Builds a final printable colored struct from a mixed value list.

- `#!ts repr.vararg(...: any): table`\
    Shortcut: `repr.construct({...})`.

- `#!ts repr.table(entries: table): table`\
    Shortcut: `repr.construct(entries)`.

## Configuration Tables

- `#!ts repr.theme: table<string, Color>`\
    Named color palette used by converters and constructors.

- `#!ts repr.replacements: table<string, string>`\
    Escape map used for string display formatting.

- `#!ts repr.conversions: table<string, function>`\
    Per-type conversion handlers used by `repr.tostring`.

## Builder Class (Module Layer)
`modules/repr.lua` registers `repr.class = class.register("repr", repr)` and adds constructor helpers:

- `#!ts repr.console(...: any): repr.object`
- `#!ts repr.chat(...: any): repr.object`
- `#!ts repr.interface(...: any): repr.object`
- `#!ts repr.custom(...: any): repr.object`

Each returns a builder object with internal buffer + network encoder.

## Builder Object API

- `#!ts obj:constructor(type: "console" | "chat" | "interface" | "custom", ...: any)`\
    Initializes message buffer and network state.

- `#!ts obj:reliable(state: boolean): self`\
    Sets reliability on underlying network encoder.

- `#!ts obj:watermark(): self`\
    Prepends `[ACRONYM]` style watermark.\
    For `interface`, toggles deferred watermark flag used client-side fallback.

- `#!ts obj:insert(...: any): self`\
    Prepends entries to buffer.\
    Aliases: `first`, `front`.

- `#!ts obj:add(...: any): self`\
    Appends entries to buffer.\
    Aliases: `last`, `back`.

- `#!ts obj:build(): self`\
    Materializes `struct` from buffer via `repr.table(...)`, strips leading color in interface mode, and writes payload into network encoder on server.

- `#!ts obj:unpack(): ...`\
    Returns unpacked built struct.

- `#!ts obj:export(): table`\
    Returns built struct table.

- `#!ts obj:print(): self?`\
    Local output behavior by type:
        - `interface` (client): UI notification.
        - `chat` (client): `chat.AddText`.
        - `custom`: `hook.Run("BSA.Repr:custom", struct)`.
        - default/console: `MsgC(..., "\n")`.

- `#!ts obj:string(): string`\
    Returns concatenated string-only content (colors ignored).

- {{ realm("server") }} `#!ts obj:channel(): string?`\
    Maps builder type to network channel:
        - `chat` -> `repr.chat`
        - `console` -> `repr.console`
        - `interface` -> `repr.interface`
        - `custom` -> `repr.custom`

- {{ realm("server") }} `#!ts obj:exclude(...: Player): self`\
    Server-only exclusion targeting.

- {{ realm("server") }} `#!ts obj:include(...: Player): self`\
    Server-only inclusion targeting.

- {{ realm("server") }} `#!ts obj:permission(...: string)`\
    Sends to players passing `BSA.Players.HasPermission(v, ...)`.\
	Alias: `permissions`.

- {{ realm("server") }} `#!ts obj:group(...: string)`\
    Sends to players whose usergroup matches provided groups.\
	Alias: `groups`.

- {{ realm("server") }} `#!ts obj:union(...: string)`\
    Sends to players matching either usergroup or permission entries.

- `#!ts obj:near(position: Vector | Entity, radius: number): self`
- `#!ts obj:send(...: Player | Player[]): self`
- `#!ts obj:broadcast(): self`
- `#!ts obj:omit(...: Player): self`
- `#!ts obj:pvs(...: any): self`
- `#!ts obj:pas(...: any): self`\
Server-side channel send helpers forwarding to underlying network encoder.

## Network Receive Behavior (Client)
Module registers client receivers:

- `repr.chat` -> `chat.AddText(unpack(buffer:table()))`
- `repr.console` -> `MsgC(unpack(buffer:table()), "\n")`
- `repr.interface` -> interface notification, or chat fallback with optional watermark reconstruction
- `repr.custom` -> `hook.Run("BSA.Repr:custom", buffer:table())`

## Notes

- Table pretty serialization is guarded and can fail-safe to error text via `repr.serialize`.
- `repr.stringify` limits iteration to first 30 keys per table level.
- Entity/player converters return readable class/name plus runtime index/id when valid.
