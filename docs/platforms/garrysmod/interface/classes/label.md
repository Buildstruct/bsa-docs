# Label
`BSA.Interface.Label` derives from `DLabel` and adds rich text fragments, wrapping, scrolling, hidden-text swapping, and sweep effects.

## Functions
- `#!ts label:SetText(...: any)`
- `#!ts label:GetText(absolute?: boolean): string|table`
- `#!ts label:SetHiddenText(...: any)`
- `#!ts label:SetFont(font: string)`
- `#!ts label:SetTextColor(color: Color)`
- `#!ts label:SetAlignment(align: number)`
- `#!ts label:SetWrapping(state: boolean)`
- `#!ts label:Wrap()`
- `#!ts label:SetScrolling(state: boolean)`
- `#!ts label:GetScrolling(): boolean`
- `#!ts label:SetPassthrough(state: boolean)`
- `#!ts label:SetSuppressOpacity(state: boolean)`
- `#!ts label:GetSuppressOpacity(): boolean`
- `#!ts label:Sweep(start_offset?: number)`
- `#!ts label:GetTextSize(): number, number`
- `#!ts label:GetContentSize(): number, number`
- `#!ts label:SizeToContentsX(add?: number)`
- `#!ts label:SizeToContentsY(add?: number)`
- `#!ts label:SizeToContents()`
- `#!ts label:IsMouseHover(): boolean`
- `#!ts label:OnHover(state: boolean)`

## Behavior
- Text input supports fragment arrays (`Color`, strings, etc.), not only plain strings.
- Hidden text is displayed when not hovered if configured via `SetHiddenText`.
- Wrapping updates automatically on width changes in both `Think` and `PerformLayout`.
