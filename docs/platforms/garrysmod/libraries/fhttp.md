# {{ realm("shared") }} FHTTP
A thin wrapper around the `HTTP` / `CHTTP` global that adds automatic retry on failure.

!!! info
	See [core/libraries/fhttp.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/fhttp.lua) for the actual design implementation.

!!! note
	FHTTP is an internal helper included locally (`include("fhttp.lua")`) rather than exposed on the `BSA` table.\
	It prefers `CHTTP` when available and falls back to the built-in `HTTP`.

## Functions

- `#!ts fhttp.HTTP(request: table, attempts?: number)`\
	Issues a standard GMod HTTP `request` and retries up to `attempts` times (default `2`) before invoking `request.failed`.\
	Wraps the request's `success`/`failed` fields to manage retry bookkeeping and clear the registry entry when done.

- `#!ts fhttp.fetch(url: string, onsuccess?: function(body: string, length: number, headers: table, code: number), onfailure?: function(err: string), header?: table)`\
	GET convenience wrapper built on `fhttp.HTTP`.\
	The success callback receives the body, its length, the response headers, and the HTTP status code.

- `#!ts fhttp.post(url: string, params: table, onsuccess?: function(body: string, length: number, headers: table, code: number), onfailure?: function(err: string), header?: table)`\
	POST convenience wrapper built on `fhttp.HTTP`.\
	`params` are sent as form parameters; the callbacks match `fetch`.
