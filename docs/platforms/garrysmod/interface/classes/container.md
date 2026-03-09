# Container
Defines two minimal container classes for generic composition.

## Classes
- `#!ts BSA.Interface.Container` (base: `DPanel`)
- `#!ts BSA.Interface.IContainer` (base: `EditablePanel`)

## Shared Functions
- `#!ts container:Sweep(start_offset?: number)`
- `#!ts container:IsMouseHover(): boolean`
- `#!ts container:PaintSweep(w: number, h: number)`
- `#!ts container:Paint(w: number, h: number)`
- `#!ts container:PerformLayout(...)`
- `#!ts container:Perform(...)`

## IContainer Accessors
- `#!ts icontainer:SetIsMenu(state: boolean)`
- `#!ts icontainer:GetIsMenu(): boolean`
- `#!ts icontainer:SetPaintBackground(state: boolean)`
- `#!ts icontainer:GetPaintBackground(): boolean`

## Behavior
- Both container classes are intentionally lightweight and primarily extension points.
- `IContainer` is used by popup/menu-like controls (dropdowns, context menus, etc.).
