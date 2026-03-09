# Dispatcher
Personalized information highways without the need of a global event system.\
This solves the problem of needing to have hooks everywhere and complicated callback systems.

Simply create a dispatcher, give it a name, and attach as many callbacks as you need.\
Names on the dispatchers themselves are for tracking purposes when debugging.

## Functions

- `#!ts dispatcher:new(name: string): dispatcher.object`\
Creates a new dispatcher routine for localized signalling.\
`__namecall` also can be used similar to `:new`.

## Object
These are returned from calling `:new` or `__namecall`.\
Responsible for holding a collection of handles to fire towards.

- `#!ts dispatcher:exists(name: string): boolean`\
Checks if the dispatcher has an existing handle.

- `#!ts dispatcher:invoke(...): ...?`\
Executes all stored handles, expecting a return if any exists.\
A return is made when the first index of any handle's return has value.\
This will prevent other handles from executing if one returns earlier than others.\
Errors within callbacks are skipped but still present the error.
    - `#!ts dispatcher:fire(...): ...?`
    - `#!ts dispatcher:call(...): ...?`
    - `#!ts dispatcher:run(...): ...?`

- `#!ts dispatcher:connect(callback: function, name?: string): dispatcher.handle`\
Adds a function callback to the designated dispatcher.\
Not providing a name will make it anonymous, so its important in that note to keep the returned handle if you plan to clean it up later.
    - `#!ts dispatcher:listen(callback: function, name?: string): dispatcher.handle`
    - `#!ts dispatcher:add(callback: function, name?: string): dispatcher.handle`
    - `#!ts dispatcher:on(callback: function, name?: string): dispatcher.handle`

- `#!ts dispatcher:disconnect(name: string): boolean`\
Removes a stored handle from the dispatcher.\
Anonymous dispatchers typically cannot be removed this way unless you managed to get their ID.
    - `#!ts dispatcher:dismiss(name: string): boolean`
    - `#!ts dispatcher:remove(name: string): boolean`
    - `#!ts dispatcher:off(name: string): boolean`

## Handle
These are returned from `dispatcher:connect(...)` and represent a single callback entry.

- `#!ts handle:invoke(...): boolean, table | string`\
Executes the stored callback through `xpcall`.
    - On success: returns `true, { ...callbackReturns }`
    - On failure: returns `false, traceback`
    - `#!ts handle:fire(...): boolean, table | string`
    - `#!ts handle:call(...): boolean, table | string`
    - `#!ts handle:run(...): boolean, table | string`

- `#!ts handle:connect(): dispatcher.handle`\
Reconnects this handle to its parent dispatcher.
    - `#!ts handle:listen(): dispatcher.handle`
    - `#!ts handle:add(): dispatcher.handle`
    - `#!ts handle:on(): dispatcher.handle`

- `#!ts handle:disconnect(): boolean`\
Disconnects this handle from its parent dispatcher.
    - `#!ts handle:dismiss(): boolean`
    - `#!ts handle:remove(): boolean`
    - `#!ts handle:off(): boolean`
