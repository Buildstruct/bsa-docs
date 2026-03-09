# ComboBox
`BSA.Interface.ComboBox` extends `BSA.Interface.DropDown` for single selection.

## Functions
- `#!ts combobox:GetSelected(): Panel?`
- `#!ts combobox:IsSelected(panel: Panel): boolean`
- `#!ts combobox:SetSelected(panel?: Panel)`
- `#!ts combobox:AddChoice(name: string): BSA.Interface.Button`
- `#!ts combobox:OnSearch(entry: Panel, text: string): boolean`
- `#!ts combobox:OnChange(old?: Panel, new?: Panel)`
- `#!ts combobox:GetValue(): string?`
- `#!ts combobox:SetValue(value: string)`
- `#!ts combobox:Clear()`

## Behavior
- Selected option text is mirrored into the collapsed control label.
- Selected option gets accent text color; previous selection is reset to white.
- Defaults to first added choice when none selected yet.
