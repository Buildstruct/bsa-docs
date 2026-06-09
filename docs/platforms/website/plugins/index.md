# Plugins

A website plugin is a class that gets loaded by the host and participates in a managed lifecycle.\
Plugins can register routes, handle cross-server commands, declare config, and optionally ship a frontend UI.

---

## Plugin sources

| Source | Location |
|---|---|
| Built-in | `backend/src/plugins/<name>/` — compiled into the binary |
| Drop-in | `plugins/<name>/` — loaded from disk at runtime (sibling of `data/`) |

A drop-in plugin with the same name as a built-in will shadow it.

---

## B1 vs B2

Plugins that ship a UI can deliver it two different ways.

| | B1 | B2 |
|---|---|---|
| Type | Build-time Svelte component | Runtime custom element |
| File | `frontend/src/plugins/<name>/window.svelte` | `<plugin>/web/<entry>.js` |
| Compiled into | The site's SPA | Nothing — served from disk |
| Can use host components | Yes | No |
| True drop-in (no rebuild) | No | Yes |

**B1** is for first-party plugins that ship with the site.\
	- It has full access to host components and stores.

**B2** is for drop-ins and third-party plugins.\
	- It's a standard custom element with no framework dependency.

Headless plugins (backend only) skip the `ui` field entirely.\
Both options register under the same `contentKey`, the host renders either one transparently.

---

## File layout

```
<name>/
    plugin.json      # descriptor
    plugin.ts        # OR plugin.js — the plugin class
    web/<entry>.js   # optional B2 UI bundle
```

---

## Lifecycle

The host calls three methods.\
All resource cleanup registered through `ctx` is automatic on disable.

| Method | When | Rules |
|---|---|---|
| `constructor(ctx)` | On enable | Synchronous only — config, routes, receivers |
| `start()` | After constructor, once DB + interlink are up | Async allowed |
| `destructor()` | On disable | Manual cleanup only (file handles, etc.) |

---

## Management API

| Endpoint | Auth | Description |
|---|---|---|
| `GET /api/plugins` | `management.plugins` | Full plugin list with config |
| `GET /api/plugins/visible` | Session (optional) | Plugins visible to the caller |
| `POST /api/plugins/set` | `management.plugins` | Enable or disable a plugin at runtime |
| `GET /api/plugins/:name/ui/*` | Plugin's own permission | Serve the B2 UI bundle |

- See [Creating a Plugin](creating.md) for the authoring guide.
- See [Context Reference](context.md) for the full `ctx` surface.
