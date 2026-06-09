# {{ realm("shared") }} NSS
Also known as "Number Super Structor", this is a big-integer helper that can go beyond 64-bits of precision.\
This is built upon 32-bit words for arbitrary-size numeric storage, with conversions, arithmetic and bitwise operations.

!!! info
	See [core/libraries/nss.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/nss.lua) for the actual design implementation.

## Internal Word Layout
NSS stores its value as a **big-endian sequence of unsigned 32-bit words**: index `1` holds the most significant word (MSW) and the last index holds the least significant word (LSW).

```lua
{
	[1]=MSW,
	[2]=...,
	[N]=LSW
}
```

!!! warning "Direct index writes"
    Code like `local s = nss:new(); s[4] = x` leaves `s[2]` and `s[3]` as `nil`, creating a sparse table.\
	`#s` may return `1` or `4` depending on LuaJIT's internal hash layout.\
	Always use `nss.fromWord` or fill every intermediate index explicitly.

An example here is creating a value with only the MSW, for example 2^97, which is 4 words.\
```lua
local v = nss.fromWord(4, 2)
print(v[1]) -- 2
print(#v) -- 4
print(v:toNamed()) -- 158.5 octillion

local v = nss:new()
v[1] = 2
v[2] = 0
v[3] = 0
v[4] = 0
print(v[1]) -- 2
print(#v) -- 4
print(v:toNamed()) -- 158.5 octillion
```

## Functions
Static constructors and coercion helpers exposed directly on the `nss` class.

- `#!ts nss.fromNumber(num: number): nss.object`\
	Builds an NSS value from a Lua number.\
	Throws if `num` is `NaN`, `+inf`, or `-inf`.

- `#!ts nss.fromBinary(str: string): nss.object`\
	Builds an NSS value from a binary string.\
	An optional `0b`/`0B` prefix is stripped.\
	Throws on non-binary characters.

- `#!ts nss.fromString(str: string): nss.object`\
	Builds an NSS value from a decimal string.\
	An optional leading sign (`+`/`-`) is accepted.\
	Throws on non-digit characters.

- `#!ts nss.fromHex(hex: string): nss.object`\
	Builds an NSS value from a hexadecimal string.\
	An optional `0x`/`0X` prefix is stripped.\
	Throws on non-hex characters.

- `#!ts nss.fromTable(words: number[]): nss.object`\
	Builds an NSS value from its raw 32-bit word array.

- `#!ts nss.fromWord(noffset: number, ndata: number): nss.object`\
	Builds an NSS value with a single `UINT32` word placed at `1` with appended zeros.

- `#!ts nss.fromAny(value: any): nss.object`\
	Coerces supported input into an NSS value.\
	Accepts existing `nss` objects, numbers, strings (decimal, `0x…` hex, `0b…` binary), and raw word tables.

- `#!ts nss.getIllionName(index: number): string`\
	Returns the short-scale illion name for the given group index (e.g. `1` → `"million"`, `2` → `"billion"`).\
	Supports arbitrarily large indices using Conway–Wechsler notation.

- `#!ts nss.getShortIllionName(index: number): string`\
	Returns the compact suffix for the given group index (e.g. `1` → `"M"`, `2` → `"B"`, `3` → `"T"`).\
	Falls back to `aa`-style notation beyond the named table.

## Object
Instances are created through the static helpers above or the underlying class constructor.

- `#!ts nss:new(words?: number[]): nss.object`\
	Creates a new NSS object from an optional raw word array.

- `#!ts nss:push(value: any)`\
	Coerces and appends another NSS value's words onto this object.

- `#!ts nss:pop(): number?`\
	Removes and returns the last raw word.

- `#!ts nss:insert(index: number, value: number)`\
	Inserts a raw word at a specific index.

- `#!ts nss:remove(index: number): number?`\
	Removes and returns the raw word at an index.

- `#!ts nss:resize(size: number)`\
	Truncates or zero-pads the internal word array to the requested size.

- `#!ts nss:size(absolute?: boolean): number`\
	Returns the number of stored 32-bit words.\
	When `absolute` is `true`, returns the total addressable bit count minus one (`words * 32 - 1`).

- `#!ts nss:clone(): nss.object`\
	Returns a copy of the current value.

- `#!ts nss:normalize(): self`\
	Removes leading zero words while preserving a single zero word for empty values.

- `#!ts nss:isZero(): boolean`\
	Returns whether the value is numerically zero.

- `#!ts nss:isNegative(): boolean`\
	Returns whether the value is negative (non-zero and sign is `-1`).

- `#!ts nss:isOdd(): boolean`\
	Returns whether the value is odd.

- `#!ts nss:isEven(): boolean`\
	Returns whether the value is even.

- `#!ts nss:applySign(sign: number): self`\
	Sets the sign to `-1` if `sign == -1`, otherwise `1`, then normalizes.

- `#!ts nss:abs(): nss.object`\
	Returns a copy of the value with a positive sign.

- `#!ts nss:negate(): nss.object`\
	Returns a copy of the value with the sign flipped.\
	Zero always remains positive.

- `#!ts nss:bitlen(): number`\
	Returns the effective bit length of the value.

- `#!ts nss:compareAbs(other: any): -1 | 0 | 1`\
	Compares the absolute magnitudes of this value and another coerced value.\
	Returns `-1`, `0`, or `1`.

- `#!ts nss:compare(other: any): -1 | 0 | 1`\
	Compares this signed value against another coerced value.\
	Returns `-1`, `0`, or `1`.

- `#!ts nss:isWithin(limit: any): boolean`\
	Returns `true` if this value is less than or equal to `limit`.\
	Alias: `fitsWithin`.

- `#!ts nss:exceeds(limit: any): boolean`\
	Returns `true` if this value is greater than `limit`.\
	Alias: `exceedsLimit`.

- `#!ts nss:bound(limit: any, fallback?: any): nss.object | nil, boolean`\
	Returns `(clone, true)` if this value is within `limit`.\
	Returns `(fallback, false)` if it exceeds `limit` and a fallback is given, otherwise `(nil, false)`.\
	Alias: `limit`.

- `#!ts nss:divmodSmall(divisor: number): nss.object, number`\
	Divides by a small Lua number and returns the quotient and the integer remainder.

- `#!ts nss:toNumber(): number`\
	Converts the value back into a Lua number.\
	Large values can exceed normal number precision.

- `#!ts nss:toString(): string`\
	Returns a decimal string representation.
	!!! warning
		Significantly slower than `toBinary()` or `toHex()`!\
		Decimal conversion requires repeated division across the internal word array.

- `#!ts nss:toBinary(): string`\
	Returns a binary string representation.

- `#!ts nss:toHex(): string`\
	Returns an uppercase hexadecimal string representation.

- `#!ts nss:toTable(): number[]`\
	Returns a copy of the internal word array.\
	Negative values include a `sign = -1` field.

- `#!ts nss:toScientific(decimals?: number): string`\
	Returns a scientific-notation string (e.g. `"1.23e6"`).\
	`decimals` defaults to `3`.\
	Trailing fractional zeros are stripped.\
	Alias: `toExponential`.

- `#!ts nss:toNamed(decimals?: number): string`\
	Returns an illion-named string (e.g. `"1.2 million"`).\
	`decimals` defaults to `1`.\
	Values below one thousand are returned as plain decimal.

- `#!ts nss:toShortNamed(decimals?: number): string`\
	Returns a illion-short-scale named string (e.g. `"1.2M"`).\
	`decimals` defaults to `1`.\
	Values below one thousand are returned as plain decimal.

## Bitwise
All operands are coerced with `nss.fromAny(...)` and return new NSS objects.

- `#!ts nss:bor(other: any): nss.object`\
	Bitwise OR.

- `#!ts nss:band(other: any): nss.object`\
	Bitwise AND.

- `#!ts nss:bnot(): nss.object`\
	Bitwise NOT over each stored 32-bit word.

- `#!ts nss:bxor(other: any): nss.object`\
	Bitwise XOR.

- `#!ts nss:lshift(bits: number): nss.object`\
	Logical left shift by an arbitrary bit count.

- `#!ts nss:rshift(bits: number): nss.object`\
	Logical right shift by an arbitrary bit count.

## Arithmetic
All operands are coerced with `nss.fromAny(...)` and return new NSS objects.

- `#!ts nss:add(other: any): nss.object`\
	Adds two values.

- `#!ts nss:sub(other: any): nss.object`\
	Subtracts another value.

- `#!ts nss:mul(other: any): nss.object`\
	Multiplies two values using 32-bit word multiplication.

- `#!ts nss:div(other: any): nss.object`\
	Returns the integer quotient of division.\
	Throws on divide by zero.

- `#!ts nss:divmod(other: any): nss.object, nss.object`\
	Returns the integer quotient and signed remainder as two values.\
	Throws on divide by zero.

- `#!ts nss:divmodAbs(other: any): nss.object, nss.object`\
	Returns the quotient and remainder of the absolute magnitudes as two values.\
	Throws on divide by zero.

- `#!ts nss:mod(other: any): nss.object`\
	Returns the signed remainder of division.

- `#!ts nss:pow(other: any): nss.object`\
	Raises the value to an exponent using binary exponentiation.\
	Throws if the exponent is negative.

- `#!ts nss:factorial(limit?: number): nss.object`\
	Returns `n!`.\
	When `limit` is provided, multiplication stops after that many iterations.
