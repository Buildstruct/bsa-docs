# Interface
Client-side UI manager for BSA, built on custom VGUI classes (`BSA.Interface.*`) with feature registration, selection, lifecycle dispatchers, and notification helpers.

UI classes are derived from Garry's Mod VGUI controls. Some methods are inherited unchanged, some are overridden, and some are BSA-specific extensions.

## Runtime Events
These are `dispatcher` instances on `BSA.Interface`.

- `#!ts interface.opened()`\
Invoked when the main interface is opened.

- `#!ts interface.closed()`\
Invoked when the main interface is closed/hidden.

- `#!ts interface.minimized()`\
Invoked when the frame is minimized.

- `#!ts interface.maximized()`\
Invoked when the frame is restored from minimized state.

## Base Feature Class (`interface.base`)
All features registered through `interface:add(...)` derive from this class unless overridden.

- `#!ts feature:constructor()`
- `#!ts feature:destructor()`
- `#!ts feature:opened()`
- `#!ts feature:closed()`
- `#!ts feature:minimized()`
- `#!ts feature:maximized()`
- `#!ts feature:selected()`
- `#!ts feature:deselected()`
- `#!ts feature:layout(w: number, h: number)`
- `#!ts feature:think(w: number, h: number)`
- `#!ts feature:isactive(): boolean`\
Returns whether the feature panel is currently visible.

- `#!ts feature:invalidatelayout(recurse?: boolean)`\
Calls `manager:InvalidateLayout(...)` for the feature panel.

## Functions
- `#!ts interface:add(name: string, struct: table): class`\
Registers a feature class as `interface.<name>` inheriting `interface.base`.
If a frame exists, the feature is inserted immediately and optionally reselected when replacing an active feature.

- `#!ts interface:remove(name: string)`\
Unregisters and removes a feature from both registry and active frame.

- `#!ts interface:select(name: string)`\
Selects a registered feature in the active frame by name.

- `#!ts interface:get(name: string, active?: boolean): class|object|nil`\
`active = false/nil`: returns registered feature class.\
`active = true`: returns active instantiated feature object from `frame.features`.

- `#!ts interface:pin(name: string, width: number, height: number, panel: Panel): DFrame`\
Creates a detached `BSA.Interface.Frame`, reparents panel content into it, and returns the pinned frame.

- `#!ts interface:build(): DFrame`\
Creates the main frame and UI layout containers if needed, then returns it.

- `#!ts interface:open(): DFrame`\
Builds (if missing), shows, restores (if minimized), focuses, and fades in the main interface.

- `#!ts interface:close()`\
Fades out and hides the interface.

- `#!ts interface:reload()`\
Rebuilds frame feature entries from the registry while preserving current permission filtering logic.

- `#!ts interface:destroy()`\
Fully removes the current frame and clears `interface.frame`.

- `#!ts interface:active(): boolean`\
True when frame exists, is visible, and is not minimized.

## Notification Helper
`interface.Notification` wraps notification access on the main frame.

- `#!ts interface.Notification:valid(): boolean`\
True if `interface.frame` is valid.

- `#!ts interface.Notification:add(...: any): any`\
Pass-through to `frame.notifications:Add(...)`.

## Registry and Ordering Notes
- `interface.registry` stores feature classes by both numeric insertion index and name key.
- `interface.spacer` captures the core feature count after `BSA.union("classes")` and `BSA.union("features")`.
- Sidebar spacing is auto-managed to visually separate core entries from plugin entries when both exist.

## Permission Filtering
When features are instantiated into the frame, they are gated by:\
- `#!ts BSA.Players.HasPermissions(LocalPlayer(), unpack(entry.permissions or {}))`

Features failing this check are skipped from the sidebar/content view.

## Network Channels and Command Behavior
Client binds these channels via `BSA.Network:receive(...)`:

- `#!ts "interface.open"` -> `interface:open()`
- `#!ts "interface.close"` -> `interface:close()`
- `#!ts "interface.toggle"` -> opens/selects tab or closes when already active and no tab argument

Also binds local command:\
- `#!ts bsa_menu [tab]`\
Mirrors toggle behavior (`tab` is lowercased before select).
