# Panel
`BSA.Interface.Panel` is a themed general-purpose panel with optional particle effects, blur, gradient, and sweep animation.

## Functions
- `#!ts panel:SetEffect(name?: string)`
- `#!ts panel:GetEffect(): string?`
- `#!ts panel:SetEffectParticleCount(count?: number)`
- `#!ts panel:GetEffectParticleCount(): number?`
- `#!ts panel:ShowGradient(state: boolean)`
- `#!ts panel:Sweep(start_offset?: number)`
- `#!ts panel:IsMouseHover(): boolean`
- `#!ts panel:Effects(w: number, h: number)`
- `#!ts panel:PaintSweep(w: number, h: number)`
- `#!ts panel:Paint(w: number, h: number)`
- `#!ts panel:PerformLayout(...)`
- `#!ts panel:Perform(...)`

## Behavior
- Effect types: `snow`, `rain`, `fire`, `sparkle`.
- If explicit effect is unset, falls back to theme (`theme:fetch("panel", "effect")`).
- `Paint` can apply blur via `theme:fetch("panel", "blur")`.
