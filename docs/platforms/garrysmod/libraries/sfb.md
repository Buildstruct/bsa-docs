# {{ realm("shared") }} SFB
Binary read/write primitives used by Flux encoders/decoders and usable standalone for custom binary protocols.\
Created by Srlion @ https://github.com/Srlion/sfs

!!! info
	See [core/libraries/sfb.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/sfb.lua) for the actual design implementation.

!!! note
	This adds a dedicated & constructed table to BSA as `SFB`.

Flux integration:

- `flux.encoder` inherits `sfb.Writer` via `__index`.
- `flux.decoder` inherits `sfb.Reader` via `__index`.

## Module Exports

- `#!lua sfb.Writer`\
	Binary writer class.

- `#!lua sfb.Reader`\
	Binary reader class.

- `#!lua sfb.NULL_ENT_INDEX: number`\
	Sentinel i16 value used to encode `NULL` entities.

## Writer

- `#!lua sfb.Writer.new(): sfb.Writer`\
	Creates a new writer buffer.

- `#!lua sfb.Writer.cached(): sfb.Writer`\
	Returns a shared cached writer reset to empty.

- `#!lua writer:reset(): self`\
	Clears buffered segments.

- `#!lua writer:tostring(): string`\
	Returns concatenated binary payload.

- `#!lua writer:data(bytes: string): self`\
	Appends raw bytes.

- `#!lua writer:string(value: string): self`\
	Writes string followed by `\0` terminator.

### Numeric Writes

- `#!lua writer:byte(n: number): self` (alias: `u8`)
- `#!lua writer:u16(n: number): self`
- `#!lua writer:u32(n: number): self`
- `#!lua writer:u53(n: number): self`
- `#!lua writer:i8(n: number): self`
- `#!lua writer:i16(n: number): self`
- `#!lua writer:i32(n: number): self`
- `#!lua writer:i53(n: number): self`
- `#!lua writer:float(n: number): self`
- `#!lua writer:double(n: number): self`
- `#!lua writer:bool(value: boolean): self`

### Garry's Mod Type Writes

- `#!lua writer:Player(ply: Player): self`
- `#!lua writer:Entity(ent: Entity | NULL): self`
- `#!lua writer:Weapon(ent: Weapon): self` (alias of `Entity`)
- `#!lua writer:Vehicle(ent: Vehicle): self` (alias of `Entity`)
- `#!lua writer:NextBot(ent: NextBot): self` (alias of `Entity`)
- `#!lua writer:NPC(ent: NPC): self` (alias of `Entity`)
- `#!lua writer:Vector(v: Vector): self`
- `#!lua writer:Angle(a: Angle): self`
- `#!lua writer:Matrix(m: VMatrix): self` (alias: `VMatrix`)
- `#!lua writer:Color(c: Color): self`

## Reader

- `#!lua sfb.Reader.new(data: string, max_size?: number): sfb.Reader`\
	Creates a reader over a byte string.

- `#!lua reader:reset(data: string, max_size?: number): self`\
	Resets reader state and input bytes.

- `#!lua reader:data(size?: number): string`\
	Reads raw bytes.\
	Without `size`, returns remaining data (bounded by `max_size`).

- `#!lua reader:string(): string`\
	Reads a null-terminated string.

### Numeric Reads

- `#!lua reader:bytes(size: number): ...number`
- `#!lua reader:u8(): number`
- `#!lua reader:u16(): number`
- `#!lua reader:u32(): number`
- `#!lua reader:u53(): number`
- `#!lua reader:i8(): number`
- `#!lua reader:i16(): number`
- `#!lua reader:i32(): number`
- `#!lua reader:i53(): number`
- `#!lua reader:float(): number`
- `#!lua reader:double(): number`
- `#!lua reader:bool(): boolean`

### Garry's Mod Type Reads

- `#!lua reader:Entity(): Entity | NULL`
- `#!lua reader:Player(): Player`
- `#!lua reader:Vector(): Vector`
- `#!lua reader:Angle(): Angle`
- `#!lua reader:Matrix(): VMatrix` (alias: `VMatrix`)
- `#!lua reader:Color(): Color`

## Notes

- SFB is byte-oriented and does not include schema/type tags by itself.
- Use matching read/write order on both ends.
- For tagged "any value" serialization, use `sfs`.
