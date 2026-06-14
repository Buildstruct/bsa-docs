# {{ realm("shared") }} Class
Class is a form of object tracking, inheritance, and metamethod overrides.\
Without the headaches of those private, public, protected, whatever...\
Extremely light weight and designed to just be simple, nothing crazy.

!!! info
	See [core/libraries/class.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/class.lua) for the actual design implementation.

!!! note
	This adds a dedicated table to BSA as `Class`.

Classes can be constructed in two ways: `namecall` or `:new()`.\
Both of which allows you to pass arguments into the constructor.\
However, `:new()` can be overwritten if you need to.

This is used as the base of all BSA related objects that need some form of tracking and inheritable traits.

## Examples
- This is how we can construct classes
```lua
local proto = {}

function proto:constructor()
	print("I am constructed!", ...)
end

function proto:destructor()
	print("I am destructed!")
end

local class_proto = class.register("example", proto)
local object = class_proto:new("hello world")
object:destructor()
```

- Class allows for metamethod overrides
```lua
local __index = {
	ex = true
}
local proto = {}
proto.__index = __index

function proto:constructor()
	print("I am constructed!", ...)
end

function proto:destructor()
	print("I am destructed!")
end

local class_proto = class.register("example", proto)
local object = class_proto:new("hello world")
object:destructor()
print(object.ex) -- true
```

## Functions

- `#!ts class.register(name: string, properties: table, base?: table): class.class`\
	This registers a new "object" that can be constructed later on with either `:new()` or just `__namecall`.

- `#!ts class.static(name: string, properties: table, base?: table): class.static`\
	This registers a new "object" without a constructor or destructor, useful for just tracking.

- `#!ts class.singleton(name: string, properties: table, base?: table): class.object`\
	Similar to `class.register` but immediately constructs it.

- `#!ts class.base(object: class.class | class.static | class.object): class.class`\
	Returns the base of the object, typically used in recursively traversing back to abstraction.

- `#!ts class.baseinvoke(object: class.class | class.static | class.object, method: string, ...: any): ...any`\
	Fetches and execute a base class function, useful for recursive functions that need its parent called.

- `#!ts class.is(object: any): boolean`\
	Checks if any type of value is considered part of the class library

- `#!ts class.is_class(object: any): boolean`\
	Checks if any type of value is considered part of the class library and is not constructed

- `#!ts class.is_object(object: any): boolean`\
	Checks if any type of value is considered part of the class library and is constructed