# {{ realm("shared") }} Autocomplete
Command tree completion, argument shadowing and resolver helpers for chatboxes and command lines.

!!! info
	See [core/libraries/autocomplete.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/autocomplete.lua) for the actual design implementation.

!!! note
	This adds a dedicated & constructed table to BSA as `Autocomplete`.

Based on the command tree from [`commands:transport()`](command.md).\
Caching/networking and permission rules are layered on by the consumer through the `:ensure()` and `:allowed()` seams.

## Functions

- `#!ts autocomplete:new(): autocomplete.object`\
	Creates an engine with an empty completer registry and no tree.

## Manager Object

- `#!ts autocomplete:feed(tree: table): self`\
	Sets the command tree to read from.

- `#!ts autocomplete:ready(): boolean`\
	`true` once a tree has been fed.

- `#!ts autocomplete:complete(input: string, ply?: Player): result`\
	Resolves input into a [result](#result).\
	`ply` defaults to `LocalPlayer()` clientside.\
	When set, entries are filtered through `:allowed`.\
	Calling the object directly is shorthand for this.

- `#!ts autocomplete:suggest(cmd: string, argStr: string): string[]`\
	full command lines for tab-completion, empty once a command resolves.

- `#!ts autocomplete:shadow(input: string, ply?: Player): string?, number?, descriptor[]?`\
	Returns `(shadow, activeIndex, arguments)` for the resolved command.

- `#!ts autocomplete:values(input: string, ply?: Player): string[], number?`\
	Opt-in argument value suggestions for custom UIs, from a registered completer or type-based defaults.

- `#!ts autocomplete:defaults(arg: table, ply?: Player): string[]`\
	Type-based default values: `boolean` -> `true/false`, `player` -> names, `select`/`multi` -> `flags.options`.

- `#!ts autocomplete:set(path: string, fn: function): self`\
	Registers a custom argument-value completer for a command path.\
	`get`/`remove` manage it.

- `#!ts autocomplete:prefix(text: string, prefixes: string[]): string, string | false`\
	Matches `text` against a list of prefixesm, returns the matched prefix and the trailing remainder, or `false` if none match.

- `#!ts autocomplete:ensure()`\
	Seam called before each lookup, hook lazy fetching/caching here.\
	No-op by default.

- `#!ts autocomplete:allowed(ply, entry: table): boolean`\
	Seam to hide entries from completions, returns `true` by default.

- `#!ts autocomplete:resolve(tokens: string[]): node?, consumed: number, path: string[], level: table?`\
	Walks the tree by tokens, `level` is the child map for further suggestions.

- `#!ts autocomplete:shadow_of(node, path): string` / `#!ts autocomplete:descriptors(node): descriptor[]` / `#!ts autocomplete:fill_children(level, base, partial, ply, out)`\
	Lower-level building blocks used by `:complete`.

## Result
Returned from `:complete(...)`.

- `completions` - tab-completable matches `{ text, full, group, node }[]`; empty once a command resolves.
- `command` - the resolved command node, or `false` while still typing the path.
- `path` - canonical resolved path names.
- `shadow` - display-only usage guide string.
- `arguments` - descriptors `{ name, label, optional, description, default }`.
- `index` - 1-based index of the argument the cursor is on.
