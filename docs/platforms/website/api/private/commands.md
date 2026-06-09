# {{ method("GET", "POST") }} Commands

Two endpoints expose the command system over HTTP.
Both sit on the private API layer and run under the identity of the authenticated player, all permission checks apply exactly as they would on any other platform.

!!! warning "Authentication"
    Both endpoints require an active `api_player` session.\
    Requests without one are rejected before reaching the handler.

---

## {{ method("GET") }} /api/private/commands

Returns the full command tree, filtered to only the commands and groups the authenticated player has permission to see.

Groups with a `permission` the player lacks are excluded entirely, including all their children.\
Commands with a `permission` the player lacks are likewise excluded.\
Nodes with no `permission` are always visible.

### Response

```json
{ "commands": CommandEntry[] }
```

#### CommandEntry

| Field | Type | Present on |
|---|---|---|
| `name` | `string` | all |
| `path` | `string[]` | all |
| `type` | `"command" \| "group"` | all |
| `description` | `string` | all |
| `aliases` | `string[]` | all |
| `permission` | `string \| undefined` | all |
| `arguments` | `Argument[]` | `"command"` only |
| `children` | `CommandEntry[]` | `"group"` only |

#### Argument

| Field | Type | Notes |
|---|---|---|
| `type` | `string` | `string`, `number`, `boolean`, `select`, `multi`, `time` |
| `optional` | `boolean` | |
| `description` | `string \| undefined` | |
| `options` | `string[] \| undefined` | Only present when the argument has a static option list (e.g. `select`, `multi`). Dynamic option resolvers are not serialized. |

### Example

```json
{
  "commands": [
    {
      "name": "ban",
      "path": ["ban"],
      "type": "command",
      "description": "Ban a player.",
      "aliases": [],
      "permission": "punishments.ban",
      "arguments": [
        { "type": "string", "optional": false, "description": "Target player" },
        { "type": "time",   "optional": false, "description": "Duration (e.g. 1d, perm)" },
        { "type": "string", "optional": true,  "description": "Reason" }
      ]
    },
    {
      "name": "server",
      "path": ["server"],
      "type": "group",
      "description": "Server management commands.",
      "aliases": [],
      "children": [
        {
          "name": "kick",
          "path": ["server", "kick"],
          "type": "command",
          "description": "Kick all players from a server.",
          "aliases": [],
          "arguments": [
            { "type": "string", "optional": false, "description": "Server name" }
          ]
        }
      ]
    }
  ]
}
```

---

## {{ method("POST") }} /api/private/commands

Executes a command string through the website API invoker.

### Request

```json
{ "command": "string" }
```

The `command` value is trimmed before execution.\
Sending a blank string after trimming returns `400`.

### Response

```json
{ "output": ["string", ...], "error": "string | null" }
```

- `output` — lines produced by the command's `reply` calls, in order
- `error` — set if the command called `throw`; `null` on success

!!! note
    A command-level error (e.g. invalid arguments, permission denied) does **not** change the HTTP status code.\
    The response is always `200` once the handler reaches execution.\
    Only malformed requests return a non-`200` status.

### Error responses

| Status | Body | Cause |
|---|---|---|
| `400` | `{ "error": "Invalid JSON body" }` | Request body is not valid JSON |
| `400` | `{ "error": "Missing \"command\" string in request body" }` | `command` field absent or not a string |
| `400` | `{ "error": "Empty command" }` | `command` is blank after trimming |
