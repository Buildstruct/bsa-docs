# Toggle
`BSA.Interface.Toggle` derives from `BSA.Interface.Label` and renders a binary switch + label.

## Functions
- `#!ts toggle:GetValue(): boolean`
- `#!ts toggle:SetValue(state: boolean)`
- `#!ts toggle:OnMousePressed()`
- `#!ts toggle:OnChange(old: boolean, new: boolean)`
- `#!ts toggle:SizeToContents()`
- `#!ts toggle:SizeToContentsX(add?: number)`
- `#!ts toggle:PaintBackground(w: number, h: number)`
- `#!ts toggle:Paint(w: number, h: number)`

## Behavior
- Left click toggles internal `b_Enable` and fires `OnChange(old, new)`.
- Draws accent half when enabled, themed inner half when disabled.
- Text can scroll when overflowed.
