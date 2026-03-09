# MultiBox
`BSA.Interface.MultiBox` extends `BSA.Interface.DropDown` for multi-selection.

## Functions
- `#!ts multibox:GetSelected(): Panel[]`
- `#!ts multibox:IsSelected(panel: Panel): boolean`
- `#!ts multibox:SetSelected(panel: Panel, state: boolean)`
- `#!ts multibox:UpdateText()`
- `#!ts multibox:AddChoice(name: string): BSA.Interface.Button`
- `#!ts multibox:OnSearch(entry: Panel, text: string): boolean`
- `#!ts multibox:OnChange(before: Panel[], after: Panel[])`
- `#!ts multibox:GetValue(): string[]`
- `#!ts multibox:SetValue(value: string, state: boolean)`
- `#!ts multibox:Reset()`
- `#!ts multibox:Clear()`

## Behavior
- Renders selected values as comma-separated label text.
- Selection toggles per item click without auto-closing popup.
- `Reset` and `Clear` both wipe selections and children; `Reset` also restores per-item text colors first.
