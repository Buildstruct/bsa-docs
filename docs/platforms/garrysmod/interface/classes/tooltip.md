# Tooltip
`BSA.Interface.ToolTip` is a floating tooltip panel plus a global hover tracker hook.

## Class
- `#!ts BSA.Interface.ToolTip` (base: `BSA.Interface.Container`)

## Functions
- `#!ts tooltip:SetText(...: any)`
- `#!ts tooltip:GetText(): string`
- `#!ts tooltip:SetMaxWidth(width: number)`
- `#!ts tooltip:MoveToMouse()`
- `#!ts tooltip:Close()`
- `#!ts tooltip:IsMouseHover(): boolean`
- `#!ts tooltip:Paint(w: number, h: number)`
- `#!ts tooltip:PerformLayout(w: number, h: number)`

## Behavior
- Global `Think` hook waits about 1 second hover delay before spawning tooltip.
- Only BSA controls with `GetToolTip()` are considered.
- Tooltip fades in/out and auto-closes when target/hover state is lost.
