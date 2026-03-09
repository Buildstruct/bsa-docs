# Image
`BSA.Interface.Image` is a lightweight material image panel with rotation, tint, and scaling controls.

## Functions
- `#!ts image:SetImage(path?: string)`
- `#!ts image:GetImage(): string?`
- `#!ts image:SetRotation(rotation: number)`
- `#!ts image:GetRotation(): number`
- `#!ts image:SetImageSize(width: number, height: number)`
- `#!ts image:SetImageColor(color: Color)`
- `#!ts image:SetAutoScale(state: boolean)`
- `#!ts image:SizeToContents()`
- `#!ts image:SizeToContentsX()`
- `#!ts image:SizeToContentsY()`

## Behavior
- Uses a simple material cache by path (`MATERIAL_CACHE`).
- Tracks actual texture dimensions (`i_ActualWidth`, `i_ActualHeight`) for `SizeToContents` methods.
- Draws centered via `surface.DrawTexturedRectRotated`.
