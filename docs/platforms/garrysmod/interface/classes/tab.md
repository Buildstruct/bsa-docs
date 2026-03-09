# Tab
Defines a themed tab control and custom property sheet.

## Classes
- `#!ts BSA.Interface.Tab` (base: `BSA.Interface.Button`)
- `#!ts BSA.Interface.PropertySheet` (base: `DPropertySheet`)

## Tab Functions
- `#!ts tab:Setup(label: string, propertySheet: Panel, panel: Panel, material?: string)`
- `#!ts tab:Paint(w: number, h: number)`
- `#!ts tab:IsActive(): boolean`
- `#!ts tab:DoClick()`
- `#!ts tab:GetTabHeight(): number`
- `#!ts tab:DragHoverClick(hoverTime: number)`
- `#!ts tab:ApplySchemeSettings()`
- `#!ts tab:Perform()`
- `#!ts tab:DoRightClick()`

## PropertySheet Functions
- `#!ts propertysheet:LeftButton(callback?: function, name?: string)`
- `#!ts propertysheet:RightButton(callback?: function, name?: string)`
- `#!ts propertysheet:GetBar(): BSA.Interface.ScrollPanel`
- `#!ts propertysheet:DoRightClick(tab?: Panel)`
- `#!ts propertysheet:PerformLayout(w: number, h: number)`
- `#!ts propertysheet:SetActiveTab(tab: Panel)`
- `#!ts propertysheet:AddSheet(label: string, panel: Panel, material?: string, noStretchX?: boolean, noStretchY?: boolean, tooltip?: string)`
- `#!ts propertysheet:CloseTab(tab: Panel, removePanelToo?: boolean): Panel`
- `#!ts propertysheet:AddContainer(label: string)`
- `#!ts propertysheet:AddBlank(label: string)`
- `#!ts propertysheet:Paint(w: number, h: number)`
- `#!ts propertysheet:OnPaint(w: number, h: number)`

## Behavior
- Replaces default tab scroller with horizontal `BSA.Interface.ScrollPanel`.
- Optional left/right bar buttons can host custom actions.
- Automatically scrolls bar to keep active tab visible.
