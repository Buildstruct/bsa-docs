# SubPanel
A collapsible section container with animated open/close behavior.

## Functions
- `#!ts subpanel:SetText(...: any)`
- `#!ts subpanel:GetText(absolute?: boolean): string|table`
- `#!ts subpanel:SetViewPort(panel: Panel)`
- `#!ts subpanel:SetSorter(callback: function)`
- `#!ts subpanel:SetPaintBackground(state: boolean)`
- `#!ts subpanel:GetPaintBackground(): boolean`
- `#!ts subpanel:Add(panel: Panel)`
- `#!ts subpanel:AddPanel(panel: Panel)`
- `#!ts subpanel:AddSpacer(): Panel`
- `#!ts subpanel:Clear()`
- `#!ts subpanel:GetContainer(): BSA.Interface.ScrollPanel`
- `#!ts subpanel:GetCanvas(): Panel`
- `#!ts subpanel:IsOpen(): boolean`
- `#!ts subpanel:Deferred()`
- `#!ts subpanel:Open()`
- `#!ts subpanel:Close()`
- `#!ts subpanel:HasAny(): boolean`
- `#!ts subpanel:IsInViewPort(): boolean`
- `#!ts subpanel:GetContractedSize(): number`
- `#!ts subpanel:GetExpandedSize(): number`
- `#!ts subpanel:OnOpen()`
- `#!ts subpanel:OnClose()`

## Behavior
- Clicking header region toggles open/closed by default.
- Open animation lerps panel height between contracted and expanded sizes.
- Defers opening until content exists unless `Deferred()` has been called.
