# {{ realm("shared") }} SFS
Tagged value serializer/deserializer for Lua and Garry's Mod runtime types.\
Designed for compact transport of mixed values (`number`, `string`, `table`, entities, vectors, colors, etc.).\
Created by Srlion @ https://github.com/Srlion/sfs

!!! info
	See [core/libraries/sfs.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/sfs.lua) for the actual design implementation.

Flux integration:

- `flux.encoder:table(...)` and `flux.encoder:any(...)` call `sfs.encode(...)`.
- `flux.decoder:table()` and `flux.decoder:any()` call `sfs.decode(...)`.

## Core Functions

- `#!lua sfs.encode(value: any, max_cache_size?: number): string | nil, err?: string`\
	Encodes one value into SFS bytes.

- `#!lua sfs.decode(bytes: string, max_size?: number): any | nil, err?: string`\
	Decodes one value from SFS bytes.

- `#!lua sfs.encode_to_hex(value: any): string | nil, err?: string`\
	Encodes a value and returns uppercase hex text.

- `#!lua sfs.decode_from_hex(hex: string): any | nil, err?: string`\
	Decodes a value from hex-encoded SFS payload.

## Custom Type Extension

- `#!lua sfs.add_custom_type(type_key: string | table, encoder: function(buf, value), decoder: function(ctx)): number`\
	Registers a custom type and returns assigned type id.

- `#!lua sfs.set_custom_type_with_id(id: number, type_key: string | table, encoder: function(buf, value), decoder: function(ctx))`\
	Binds a custom type to an explicit id (for deterministic cross-realm/protocol compatibility).

## Constants and Namespaces

- `#!lua sfs.TYPES: table`\
	Internal type id registry (`name -> { start, max }`).

- `#!lua sfs.STRING_TYPES: table<number, true>`\
	Lookup table for string-tag byte ids.

- `#!lua sfs.VERSION: string`\
	Current library version.

- `#!lua sfs.Encoder`\
	Advanced low-level encoder namespace (exposed for custom integrations).

- `#!lua sfs.Decoder`\
	Advanced low-level decoder namespace (exposed for custom integrations).

## Buffer Utilities

- `#!lua sfs.new_buffer(): table`\
	Creates a raw encoder buffer (`[0]` length slot).

- `#!lua sfs.end_buffer(buf: table): string`\
	Concatenates a raw buffer into bytes.

- `#!lua sfs.reset_buffer(buf: table)`\
	Resets raw buffer length to zero.

## Advanced Runtime Hook

- `#!lua sfs.set_type_function(fn: function(value): string | table)`\
	Overrides the type resolver used by encoder dispatch.\
	Intended for advanced/custom environments.

## Developer Notes

- `sfs.encode/decode` are the main APIs most addon code should use.
- `sfs` is schema-less: decoder expects exactly one encoded value starting at byte 1.
- Keep custom type ids synchronized across server/client when using manual ids.
