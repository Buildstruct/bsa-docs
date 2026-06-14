# {{ realm("server") }} Commands
Runtime command tree system with pluggable interfaces, argument parsing/validation, permission hooks, and recursive group routing.

!!! info
	See [core/libraries/command.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/command.lua) for the actual design implementation.

!!! note
	This adds a dedicated & constructed table to BSA as `Commands`.

## Functions

- `#!ts commands:new(): commands.object`\
Creates a command manager, registers baseline argument types, and initializes dispatchers.

## Manager Object

- `#!ts commands:phrase(key: string, ...): string`\
Resolves text from `manager.phrases` and applies `string.format` when arguments are provided.

- `#!ts commands:argument(name: string, callback: function): commands.argument`\
Registers/replaces an argument parser by name.

- `#!ts commands:handle(interface: commands.interface, entity?: any): commands.invoker`\
Creates an invoker bound to interface + source entity/custom data.

- `#!ts commands:interface(name: string, struct?: table): commands.interface`\
Creates an interface instance and optionally overrides methods with `struct`.

- `#!ts commands:add(name: string): commands.functional`\
Adds/replaces a root-level functional command.

- `#!ts commands:remove(name: string)`\
Removes a root-level command/group entry.

- `#!ts commands:group(name: string): commands.group`\
Gets or creates a root-level command group.

- `#!ts commands:flatten(children?: table, out?: table): table`\
Returns flattened ordered list of groups/commands recursively.

- `#!ts commands:transport(children?: table, out?: table): table`\
Builds a serializable tree snapshot (name, aliases, args, desc, permissions, flattened flags).

- `#!ts commands:prefix(text: string, prefixes: string[]): string | false, string?`\
Matches first prefix and returns `(prefix, remainder)` or `false`.

- `#!ts commands:find(...path: string): commands.functional | false`\
Finds nested functional command by exact path segments.

## Manager Events

- `#!ts commands.permission(node: commands.group | commands.functional, permission: string)`\
Fired when permissions are added through `.permission(...)`.

- `#!ts commands.added(node: commands.group | commands.functional)`\
Fired when command/group is created.

- `#!ts commands.removed(node: commands.group | commands.functional)`\
Fired when command/group is removed.

- `#!ts commands.refreshed(old_node: commands.group | commands.functional, new_node: commands.group | commands.functional)`\
Fired when a same-name node is replaced.

- `#!ts commands.invoked(command: commands.functional, invoker: commands.invoker, raw_args: string[], parsed_args: any[])`\
Fired after argument validation succeeds and before callback execution.

## Hooks

- `#!ts BSA.Commands:invoked(command: commands.functional, invoker: commands.invoker, raw_args: string[], parsed_args: any[])`\
Fired after argument validation succeeds and before callback execution.\
Useful if you need to log commands.

## Functional Command
Created through `group:command(...)` or manager-level `commands:add(...)`.

- `#!ts command:serveronly(state: boolean): self`\
Blocks invocation from serverless interfaces when `true`.

- `#!ts command:playeronly(state: boolean): self`\
Requires a valid invoker entity when `true`.

- `#!ts command:alias(...aliases: string): self`
- `#!ts command:permission(...perms: string): self`
- `#!ts command:permissions(): string[]`
- `#!ts command:callback(cb?: function): self | function`
- `#!ts command:condition(cb?: function(self, invoker, next: function(state: boolean, reason?: string))): self | function`
- `#!ts command:description(text?: string): self | string`
- `#!ts command:argument(type: string, flags?: table): self`
- `#!ts command:arguments(): table[]`

- `#!ts command:validate(invoker: commands.invoker, ...raw: string): boolean, any[] | string, string?`\
Runs argument parsers declared in `meta.arguments`.\
Returns `(true, parsedArgs)` or `(false, userError, criticalTraceback?)`.

- `#!ts command:invoke(invoker: commands.invoker, ...raw: string): boolean, string?, string?`\
Executes player/server guards, validation, emits `commands.invoked`, then runs callback via `xpcall`.\
On parser/callback error returns `(false, reason, critical?)`.

- `#!ts command:path(concat?: boolean): string[] | string`
- `#!ts command:list(): table`
- `#!ts command:phrase(...): string`
- `#!ts command:throw(...)`
- `#!ts command:reply(...)`
- `#!ts command:rreply(...)`
- `#!ts command:message(targets, ...)`
- `#!ts command:rmessage(targets, ...)`\
Proxy output helpers routed through active invoker/interface.

## Group
Hierarchical command container.

- `#!ts group:group(name: string): commands.group`\
Creates nested group.

- `#!ts group:category(name: string): commands.group`\
Alias of `group:group(...)`.

- `#!ts group:command(name: string): commands.functional`\
Creates/replaces child command.

- `#!ts group:add(name: string): commands.functional`\
Alias of `group:command(...)`.

- `#!ts group:remove(name: string)`\
Removes child command/group.

- `#!ts group:flattenize(): self`\
Marks group as flattened alias scope for interface resolver.

- `#!ts group:alias(...aliases: string): self`
- `#!ts group:permission(...perms: string): self`
- `#!ts group:permissions(): string[]`
- `#!ts group:condition(cb?: function(self, invoker, next: function(state: boolean, reason?: string))): self | function`
- `#!ts group:description(text?: string): self | string`
- `#!ts group:path(concat?: boolean): string[] | string`
- `#!ts group:list(): table`
- `#!ts group:phrase(...): string`

## Interface
Input adapter that parses a text message and routes to command tree.

- `#!ts interface:invoke(invoker: commands.invoker, message: string)`\
	Resolves aliases/groups/flattened groups, runs access conditions, then invokes resolved command.

- `#!ts interface:handle(entity?: any): commands.invoker`\
	Shortcut for `manager:handle(interface, entity)`.

- `#!ts interface:condition(invoker, command, next)`\
	Global interface access hook.\
	Default `next(true)`.

- `#!ts interface:failure(invoker, command, err)`\
	Called for user-facing command failure reasons.

- `#!ts interface:error(invoker, command, critical)`\
	Called for internal/traceback failures.

### Required Overrides

- `#!ts interface:reply(invoker, command, ...)`
- `#!ts interface:rreply(invoker, command, ...)`
- `#!ts interface:message(invoker, command, targets, ...)`
- `#!ts interface:rmessage(invoker, command, targets, ...)`
- `#!ts interface:username(invoker): string`
- `#!ts interface:identifier(invoker): string`
- `#!ts interface:groups(invoker, cb)`
- `#!ts interface:primary(invoker, cb)`
- `#!ts interface:secondary(invoker, cb)`
- `#!ts interface:can(invoker, other, permissions: string[], cb)`
- `#!ts interface:has(invoker, permissions: string[], cb)`\
`invoker:throw(...)` also expects your interface to implement `throw(...)`.

### Invoker
Runtime execution context passed to command callbacks.

- `#!ts invoker:type(): string`
- `#!ts invoker:serverless(): boolean`
- `#!ts invoker:setsilent(state: boolean)`
- `#!ts invoker:issilent(): boolean`
- `#!ts invoker:username(): string`
- `#!ts invoker:identifier(): string`
- `#!ts invoker:phrase(...): string`
- `#!ts invoker:throw(...)`
- `#!ts invoker:reply(...)`
- `#!ts invoker:rreply(...)`
- `#!ts invoker:message(...)`
- `#!ts invoker:rmessage(...)`
- `#!ts invoker:groups(cb)`
- `#!ts invoker:primary(cb)`
- `#!ts invoker:secondary(cb)`
- `#!ts invoker:can(other, permissions: string | string[], cb)`
- `#!ts invoker:has(permissions: string | string[], cb)`

## Argument Objects
Created by `commands:argument(...)`.

- `#!ts argument.name: string`
- `#!ts argument.callback(command, argument, invoker, flags, input: string[], index: number): boolean, any?, number?`\
Expected return contract:
`true, parsedValue, consumedOffset?` on success;\
`false, userError` on parse/validation failure.\
Thrown errors become internal failures (`functional.argument.internal`).

Argument utilities:
- `#!ts argument:destructor()`
- `#!ts argument:phrase(key, ...): string`

### Built-In Arguments
Registered by `commands:baseline()`.

- `#!ts number`\
	`tonumber` parse with `flags.min`, `flags.max`, `flags.round`, `flags.default`, `flags.optional`.

- `#!ts string`\
	Supports quoted multi-word parsing; optional/default behavior.

- `#!ts select`\
	Single value from `flags.options`.

- `#!ts multi`\
	Comma-separated values from `flags.options`; supports `flags.min`/`flags.max`.

- `#!ts boolean`\
	Truthy only for `"1"` or `"true"` (string forms); otherwise false/default/optional path.

- `#!ts color`\
	Accepts `R,G,B[,A]` or hex `#RRGGBB[AA]`.

- `#!ts vector`\
	Accepts `X,Y,Z`.

- `#!ts angle`\
	Accepts `P,Y,R`.

- `#!ts time`\
	Accepts absolute seconds or tokenized units (`y`, `mo`, `w`, `d`, `h`, `m`, `s`).\
	Helper exposed as `commands.to_seconds(value)`.

- `#!ts player`\
	Supports selector expressions with RPN operators `+`, `-`, `!`, parentheses.\
	Supports prefixes:
	`@` aimed player, `^` self, `*` all, `$` steam id lookup, `#` usergroup, `&` radius, `?` random count.\
	Flags include `single`, `limit`, `filter`, `default`, `optional`.

- `#!ts entity`\
	Same expression model as `player`, but for entities.\
	Prefixes:
	`@` aimed entity, `^` self entity, `*` all entities, `#` class find, `$` entity index, `&` radius.

- `#!ts steam`\
	Accepts SteamID, SteamID64, or profile URL.\
	`^` resolves invoker steamid64.

#### Picker extension

- `#!ts commands.arguments.player:add_picker(prefix: string, cb)`
- `#!ts commands.arguments.player:get_picker(prefix: string)`
- `#!ts commands.arguments.player:remove_picker(prefix: string)`
- `#!ts commands.arguments.entity:add_picker(prefix: string, cb)`
- `#!ts commands.arguments.entity:get_picker(prefix: string)`
- `#!ts commands.arguments.entity:remove_picker(prefix: string)`

## sRPN Parser
Set-expression engine used by `player`/`entity` arguments.

- `#!ts commands.sRPN:tokenize(text: string): token[]`
- `#!ts commands.sRPN:parse(tokens: token[]): token[] | false, string`
- `#!ts commands.sRPN:eval(rpn: token[], ...): table | false, string`\
`identifier(...)` and `iterator(...)` are expected to be overridden by concrete engines.
