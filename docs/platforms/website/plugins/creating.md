# Creating a Plugin

## 1. Write `plugin.json`

The host reads this without executing any plugin code, so it works even when the plugin is disabled.

```json
{
  "alias": "My Plugin",
  "description": "What this plugin does.",
  "permission": "utility.myplugin",
  "ui": { "entry": "myplugin.js", "contentKey": "myplugin", "icon": "IconTerminal" }
}
```

- `alias`, `description` — shown in the management window.
- `permission` — an existing BSA permission. Holders of it can see and access the plugin.
- `ui` — omit entirely for a headless (backend-only) plugin.

The plugin name is its directory name. Keep it stable — it becomes the config key and persistence path.

## 2. Write the class

```ts
import type { PluginContext, PluginInstance } from '../../base/plugin-sdk';

export default class MyPlugin implements PluginInstance {
    constructor(private readonly ctx: PluginContext) {
        // Sync only: config, routes, receivers.
    }

    async start(): Promise<void> {
        // DB and interlink are up here. Async work goes here.
    }

    destructor(): void {
        // Teardown for anything ctx cannot track.
    }
}
```

!!! danger
    A drop-in plugin must not import host modules by path — the host is inside the compiled binary.\
    Everything runtime is reached through `ctx`.

## 3. Declare config

Build the config schema in the constructor. An `enabled` boolean is always created for you.

```ts
constructor(private readonly ctx: PluginContext) {
    if (!ctx.config.find('console')) {
        ctx.config.add('boolean', 'console', { alias: 'Echo to console', default: true });
    }
}
```

Guard with `if (!ctx.config.find(...))` — config is restored from disk before the constructor runs, so rebuilding unconditionally would overwrite saved values.

## 4. Register permissions

Permissions are database-backed. Register them once the database is up, not in the constructor.

```ts
async start(): Promise<void> {
    this.ctx.interlink.onConnected(() => {
        void this.ctx.permissions.add('utility.myplugin', 'View My Plugin');
    });
}
```

`ctx.permissions.add` is idempotent — calling it on every connect is safe.

## 5. Register routes

Routes registered through `ctx.route` are dropped automatically when the plugin is disabled.

```ts
this.ctx.route.get('/api/plugin/myplugin/data', (_req, rctx) => {
    return Response.json({ ok: true });
});
```

No options → inherits the plugin's declared permission. Pass `{}` for a public endpoint.

## 6. B1 frontend (build-time)

Ship `frontend/src/plugins/<name>/window.svelte`. Compiled into the SPA — can import host components and stores directly.

```svelte
<script lang="ts">
    import { api } from '$lib/core/api';
    let { data, setData }: { data?: unknown; setData?: (d: unknown) => void } = $props();
</script>
```

## 7. B2 frontend (runtime drop-in)

Ship `web/<entry>.js` as a custom element. Works in the compiled binary without a frontend rebuild.

```js
class MyPluginUI extends HTMLElement {
    connectedCallback() { this.innerHTML = '…'; }
    set data(v) { /* restored window state */ }
    set setData(fn) { /* call fn(state) to persist state */ }
}
customElements.define('bsa-plugin-myplugin', MyPluginUI);
```

Use `data` / `setData` to persist a small JSON snapshot (filters, scope, active view) across sessions. Do not persist scroll positions or fetched rows.
