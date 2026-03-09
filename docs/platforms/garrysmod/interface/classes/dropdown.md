# DropDown
`BSA.Interface.DropDown` derives from `BSA.Interface.Button` and manages a popup option container.

## Functions
- `#!ts dropdown:ShowSearch(state: boolean)`
- `#!ts dropdown:SetText(...: any)`
- `#!ts dropdown:GetText(absolute?: boolean): string|table`
- `#!ts dropdown:OnSearch(entry: Panel, text: string): boolean`
- `#!ts dropdown:SetMaxHeight(height: number)`
- `#!ts dropdown:GetMaxHeight(): number`
- `#!ts dropdown:IsOpen(): boolean`
- `#!ts dropdown:Open(): BSA.Interface.ScrollPanel`
- `#!ts dropdown:Close()`
- `#!ts dropdown:OnOpen()`
- `#!ts dropdown:OnClose()`
- `#!ts dropdown:GetOptions(): Panel[]`
- `#!ts dropdown:AddPanel(panel: Panel): Panel`
- `#!ts dropdown:AddButton(name: string, callback?: function(dropdown))`
- `#!ts dropdown:Clear()`
- `#!ts dropdown:Generate()`
- `#!ts dropdown:PerformContainerLayout()`

## Behavior
- Popup is an `BSA.Interface.IContainer` registered as menu component for derma close handling.
- Optional search box filters visibility using `OnSearch`.
- Tracks options in `m_Children` whether popup is currently open or closed.
