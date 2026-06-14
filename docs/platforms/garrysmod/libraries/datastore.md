# {{ realm("server") }} Datastore
Database manager abstraction over multiple SQL engines (currently `sqlite` and `mysqloo`) with unified lifecycle/events, query helpers, and optional localized modules.

!!! info
	See [core/libraries/datastore.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/datastore.lua) for the actual design implementation.

!!! danger
	We highly recommend using transactions and prepared statements for input-based queries.\
	Not doing so will leave you susceptible to SQL injection attacks due to human error.

!!! note
	This adds a dedicated & constructed table to BSA as `Datastore`.

## Functions

- `#!ts datastore:new(engine: "sqlite" | "mysqloo", config?: table): datastore.object`\
	Creates a datastore manager and underlying SQL wrapper instance.

## Manager Object

- `#!ts datastore:engine(): datastore.sql`\
	Returns underlying engine object.

- `#!ts datastore:alive(): boolean`\
	Returns connection/alive state from engine.

- `#!ts datastore:connect(callback?: function(state: boolean, err?: string))`\
	Starts engine connection flow.

- `#!ts datastore:disconnect()`\
	Disconnects engine.

- `#!ts datastore:type(): string`\
	Returns engine class/type name.

- `#!ts datastore:query(sql: string, format?: table, callback?: function(data | false, err?: string))`\
	Executes raw query with optional `%` formatting array.\
	String values in `format` are escaped automatically.

- `#!ts datastore:prepare(sql: string)`\
	Returns prepared statement object on engines that support it (`mysqloo`).\
	SQLite throws unsupported error.

- `#!ts datastore:pquery(sql: string, params?: table, callback?: function(data | false, err?: string))`\
	Prepared query shortcut (`prepare(...):run(...)`) on supporting engines.\
	SQLite throws unsupported error.

- `#!ts datastore:transaction()`\
	Creates transaction object bound to engine.

- `#!ts datastore:escape(value: string, no_quotes?: boolean): string`\
	Escapes SQL value through engine implementation.

- `#!ts datastore:localize(id: string, struct: table): datastore.localize`\
	Registers and constructs a localized module bound to this datastore.

## Manager Events
All are `dispatcher` objects.\
Return values are ignored.

- `#!ts datastore.connected(...)`\
	Forwarded from engine `connected`.

- `#!ts datastore.disconnected(...)`\
	Forwarded from engine `disconnected`.

- `#!ts datastore.queue(query: string | object)`\
	Fired when query/statement/transaction query is queued.

- `#!ts datastore.failure(err: string)`\
	Connection-level failure event.

- `#!ts datastore.error(query: string | object, err: string, traceback?: string)`\
	Query/runtime error event.

## SQL Namespace
Engine wrapper registry used internally by `datastore:new(...)`.

- `#!ts datastore.SQL.types(): string[]`\
	Returns registered engine ids.

- `#!ts datastore.SQL.register(id: string, struct: table): class`\
	Registers engine class inheriting `datastore.sql`.

- `#!ts datastore.SQL.new(id: string, ...): datastore.sql`\
	Constructs registered engine instance.

## Base Engine Contract (`datastore.sql`)
Engine wrappers implement/override these methods.

- `#!ts engine:connect(callback?)`
- `#!ts engine:disconnect()`
- `#!ts engine:alive(): boolean`
- `#!ts engine:query(sql, format?, callback?)`
- `#!ts engine:prepare(sql)`
- `#!ts engine:pquery(sql, params?, callback?)`
- `#!ts engine:transaction()`
- `#!ts engine:escape(value, no_quotes?): string`
- `#!ts engine:type(): string`
- `#!ts engine:connected(...)`
- `#!ts engine:disconnected(...)`
- `#!ts engine:failure(err)`
- `#!ts engine:error(query, err, traceback?)`

## SQLite Wrapper (`sqlite`)

- Always `alive() == true`.
- `connect(cb)` is deferred to next tick and immediately succeeds.
- `query(...)` executes via `sql.Query`.
- `prepare` / `pquery` are unsupported and throw errors.
- `escape` uses `SQLStr`.

### SQLite Query Callback
- Success: `callback(data)` where `data` is query result or `nil` (engine-dependent).
- Failure: `callback(false, sql.LastError())`.

### SQLite Transaction

- `#!ts tx:query(sql: string, format?: table)`\
	Buffers formatted query.

- `#!ts tx:pquery(...)`\
	Unsupported (throws).

- `#!ts tx:count(): number`
- `#!ts tx:get(): string` (newline-joined SQL)
- `#!ts tx:trace(): string`
- `#!ts tx:commit(callback?: function(), wait?: any)`\
	Runs buffered queries in transaction.\
	Rolls back on first failure.

## MySQLOO Wrapper (`mysqloo`)

Config required in constructor:

- `Host: string`
- `Username: string`
- `Password: string`
- `Schema: string`
- `Port: number`

Behavior:

- `connect(cb)` initializes mysqloo connection and wires native callbacks.
- `disconnect()` calls `database:disconnect(true)`.
- `alive()` checks mysqloo database status.
- `query(...)` returns a mysqloo query object and starts it immediately.
- `prepare(sql)` returns statement runner with `:run(params, callback?)`.
- `pquery(sql, params, callback?)` is `prepare+run` shortcut.
- `escape(value, no_quotes?)` uses `database:escape`.

### MySQLOO Query Object Additions
For normal/prepared query objects created by wrapper:

- `#!ts q:get(): string` (original SQL text)
- `#!ts q:trace(): string` (captured traceback)
- `#!ts q:isQuery(): true`
- `#!ts q:isTransaction(): false`

### MySQLOO Query Callback
- Success: `callback(data)`\
For multi-query results, callback receives aggregated list of result sets.
- Failure: `callback(false, err)` and `datastore.error` is fired.

### MySQLOO Prepared Params
Supported parameter types by index:

- `number` -> `setNumber`
- `string` -> `setString`
- `boolean` -> `setBoolean`
- `nil` -> `setNull`
  
Unsupported types throw an error.\
Parameter overflow against `?` placeholder count throws.

### MySQLOO Transaction

- `#!ts tx:query(sql: string, format?: table, callback?: function): self`\
	Appends raw query object to transaction.

- `#!ts tx:pquery(sql: string, params?: table): self`\
	Appends prepared query object to transaction.

- `#!ts tx:get(as_string?: boolean): table | string`
- `#!ts tx:trace(): string`
- `#!ts tx:count(): number`
- `#!ts tx:isTransaction(): true`
- `#!ts tx:isQuery(): false`
- `#!ts tx:commit(callback?: function(data | false, err?: string), wait?: boolean)`\
	Starts transaction and optionally blocks with `wait`.

## Localized Storage (`datastore.localize`)
Per-datastore module class that receives forwarded lifecycle/query events.

Hooks to override:

- `#!ts local:connected()`
- `#!ts local:disconnected()`
- `#!ts local:queue(query)`
- `#!ts local:failure(err)`
- `#!ts local:error(query, err)`

Helpers:

- `#!ts local:engine()`
- `#!ts local:alive()`
- `#!ts local:type()`
- `#!ts local:query(...)`
- `#!ts local:prepare(...)`
- `#!ts local:pquery(...)`
- `#!ts local:transaction()`
- `#!ts local:escape(value, no_quotes?)`

## Notes

- Query formatting helper escapes only string values passed via `format` array and then applies `string.format`.