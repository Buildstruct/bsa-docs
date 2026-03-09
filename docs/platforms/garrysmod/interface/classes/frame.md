# Frame
Defines two frame classes: a lightweight frame panel and the main custom frame.

## Classes
- `#!ts BSA.Interface.LightFrame` (base: `DPanel`)
- `#!ts BSA.Interface.Frame` (base: `DFrame`)

## LightFrame Functions
- `#!ts lightframe:Paint(w: number, h: number)`
- `#!ts lightframe:PerformLayout(...)`
- `#!ts lightframe:Perform(...)`

## Frame Functions
- `#!ts frame:IsMinimized(): boolean`
- `#!ts frame:SetPhased(state: boolean)`
- `#!ts frame:GetPhased(): boolean`
- `#!ts frame:RememberOrigin(state: boolean)`
- `#!ts frame:GetCanvas(): Panel`
- `#!ts frame:GetContainer(): Panel`
- `#!ts frame:SetTitle(...: any)`
- `#!ts frame:GetTitle(absolute?: boolean): string|table`
- `#!ts frame:SetMaxWidth(n: number)`
- `#!ts frame:SetMaxHeight(n: number)`
- `#!ts frame:SizeToContents()`
- `#!ts frame:SizeToContentsX()`
- `#!ts frame:SizeToContentsY()`
- `#!ts frame:ShowCloseButton(show: boolean)`
- `#!ts frame:SetImage(path?: string)`
- `#!ts frame:SetIcon(path?: string)`
- `#!ts frame:AddICOPanel(iconPanel: Panel)`
- `#!ts frame:SetEffect(name?: string)`
- `#!ts frame:GetEffect(): string?`
- `#!ts frame:SetEffectParticleCount(count?: number)`
- `#!ts frame:GetEffectParticleCount(): number?`
- `#!ts frame:Effects(w: number, h: number)`
- `#!ts frame:Close()`
- `#!ts frame:OnClose()`
- `#!ts frame:OnMinimized(state: boolean)`
- `#!ts frame:Perform()`

## Behavior
- Replaces default `DFrame` title/controls with BSA label/buttons.
- Minimize mode shrinks to title-bar footprint and can restore origin position.
- "Phased" mode fades frame and disables input when not hovered.
- Supports frame particle effects (`snow`, `rain`, `fire`, `sparkle`) with optional explicit particle count.
- `Close()` fades out, hides, then removes when `DeleteOnClose` is enabled.
