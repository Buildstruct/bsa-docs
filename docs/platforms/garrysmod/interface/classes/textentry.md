# TextEntry
Defines both a direct themed text entry and a wrapper variant.

## Classes
- `#!ts BSA.Interface.TextEntryObject` (base: `DTextEntry`)
- `#!ts BSA.Interface.TextEntry` (base: `DTextEntry`)

## TextEntryObject Functions
- `#!ts textentryobject:GetValue(): string`
- `#!ts textentryobject:SetValue(value: string)`
- `#!ts textentryobject:PaintBackground(w: number, h: number)`
- `#!ts textentryobject:Paint(w: number, h: number)`

## TextEntry Functions
- `#!ts textentry:SetPaintBackground(state: boolean)`
- `#!ts textentry:GetPaintBackground(): boolean`
- `#!ts textentry:SetPlaceholderText(text: string)`
- `#!ts textentry:GetPlaceholderText(): string`
- `#!ts textentry:SetText(text: string)`
- `#!ts textentry:GetText(): string`
- `#!ts textentry:SetNumeric(state: boolean)`
- `#!ts textentry:GetNumeric(): boolean`
- `#!ts textentry:AddHistory(value: string)`
- `#!ts textentry:SetCursorColor(color: Color)`
- `#!ts textentry:GetCursorColor(): Color`
- `#!ts textentry:SetEditable(state: boolean)`
- `#!ts textentry:GetEditable(): boolean`
- `#!ts textentry:SetFont(font: string)`
- `#!ts textentry:GetFont(): string`
- `#!ts textentry:SetHighlightColor(color: Color)`
- `#!ts textentry:GetHighlightColor(): Color`
- `#!ts textentry:SetTextColor(color: Color)`
- `#!ts textentry:GetTextColor(): Color`
- `#!ts textentry:SetEnterAllowed(state: boolean)`
- `#!ts textentry:GetEnterAllowed(): boolean`
- `#!ts textentry:SetMultiline(state: boolean)`
- `#!ts textentry:GetMultiline(): boolean`
- `#!ts textentry:SetIcon(iconPath?: string)`
- `#!ts textentry:GetIcon(): string?`
- `#!ts textentry:GetValue(): string`
- `#!ts textentry:SetValue(value: string)`
- `#!ts textentry:OnChange(...)`
- `#!ts textentry:OnTextChanged(...)`
- `#!ts textentry:OnEnter(...)`

## Behavior
- Wrapper relays underlying `TextEntryObject` callbacks into `OnTextChanged` and `OnChange`.
- Supports optional left icon and adjusts inner text-entry bounds in `PerformLayout`.
- Accent color is applied to cursor/highlight each paint pass.
