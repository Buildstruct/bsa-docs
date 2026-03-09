# Button
`BSA.Interface.Button` derives from `BSA.Interface.Label` and adds clickable button behavior with optional icon/image support.

## Functions
- `#!ts button:IsDown(): boolean`
- `#!ts button:IsHovered(): boolean`
- `#!ts button:PaintBackground(w: number, h: number)`
- `#!ts button:Paint(w: number, h: number)`
- `#!ts button:Calibrate()`
- `#!ts button:SizeToContentsY(add?: number): number`
- `#!ts button:SizeToContentsX(add?: number): number`
- `#!ts button:SizeToContents(): number, number`
- `#!ts button:SetImageRotation(rotation: number)`
- `#!ts button:SetImage(path?: string)`
- `#!ts button:SetIcon(path?: string)` (alias of `SetImage`)
- `#!ts button:SetMaterial(mat?: IMaterial)`
- `#!ts button:PerformLayout(w: number, h: number)`
- `#!ts button:Perform()`

## Behavior
- Supports passthrough-hover children (`label:SetPassthrough(true)`) when resolving hover state.
- Draws selected underline when `button.selected` is truthy.
- Supports horizontal text scrolling when `SetScrolling(true)` and text overflows.
- Auto-scales icon/image to fit button bounds in `PerformLayout`.
