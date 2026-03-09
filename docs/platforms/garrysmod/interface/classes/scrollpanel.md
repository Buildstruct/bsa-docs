# ScrollPanel
Provides the full custom scroll stack.

## Classes
- `#!ts BSA.Interface.ScrollVBar` (base: `BSA.Interface.Container`)
- `#!ts BSA.Interface.ScrollHBar` (base: `BSA.Interface.Container`)
- `#!ts BSA.Interface.ScrollCanvas` (base: `BSA.Interface.Container`)
- `#!ts BSA.Interface.ScrollPanel` (base: `BSA.Interface.IContainer`)

## ScrollCanvas Functions
- `#!ts scrollcanvas:Index(panel: Panel): number|false`
- `#!ts scrollcanvas:Add(panel: Panel)`
- `#!ts scrollcanvas:Insert(index: number, panel: Panel)`
- `#!ts scrollcanvas:Move(panel: Panel, index: number)`
- `#!ts scrollcanvas:Sort(callback: function)`
- `#!ts scrollcanvas:First(): Panel?`
- `#!ts scrollcanvas:Last(): Panel?`
- `#!ts scrollcanvas:Count(): number`
- `#!ts scrollcanvas:GetChildren(absolute?: boolean): Panel[]`

## ScrollPanel Functions
- `#!ts scrollpanel:SetHorizontal(state: boolean)`
- `#!ts scrollpanel:SetPadding(padding: number)`
- `#!ts scrollpanel:GetPadding(): number`
- `#!ts scrollpanel:SetSpacing(spacing: number)`
- `#!ts scrollpanel:GetSpacing(): number`
- `#!ts scrollpanel:SetBarVisible(state: boolean)`
- `#!ts scrollpanel:GetBar(): Panel`
- `#!ts scrollpanel:SetViewPort(panel: Panel)`
- `#!ts scrollpanel:SetScrollSize(value: number)`
- `#!ts scrollpanel:Add(panel: Panel): Panel`
- `#!ts scrollpanel:AddPanel(panel: Panel): Panel`
- `#!ts scrollpanel:Insert(index: number, panel: Panel)`
- `#!ts scrollpanel:Move(panel: Panel, index: number)`
- `#!ts scrollpanel:Clear()`
- `#!ts scrollpanel:Release()`
- `#!ts scrollpanel:GetCanvas(): Panel`
- `#!ts scrollpanel:GetCanvasSize(): number`
- `#!ts scrollpanel:GetLength(): number`
- `#!ts scrollpanel:GetTypicalSize(): number`
- `#!ts scrollpanel:GetWide(min?: number): number`
- `#!ts scrollpanel:GetCount(): number`
- `#!ts scrollpanel:GetFirst(): Panel?`
- `#!ts scrollpanel:GetLast(): Panel?`
- `#!ts scrollpanel:HasAny(): boolean`
- `#!ts scrollpanel:IsFull(): boolean`
- `#!ts scrollpanel:CanScroll(): boolean`
- `#!ts scrollpanel:GetScroll(): number`
- `#!ts scrollpanel:SetScroll(pixels: number, process?: boolean)`
- `#!ts scrollpanel:MoveTo(pixels: number, process?: boolean)`
- `#!ts scrollpanel:ScrollToChild(target: Panel)`
- `#!ts scrollpanel:GetPosition(target: Panel, absolute?: boolean): number`
- `#!ts scrollpanel:IsRendering(target: Panel, padding?: number): boolean`
- `#!ts scrollpanel:SetSorter(callback: function)`
- `#!ts scrollpanel:SetPrevent(state: boolean)`
- `#!ts scrollpanel:Process()`
- `#!ts scrollpanel:Think()`
- `#!ts scrollpanel:OnThink()`
- `#!ts scrollpanel:PerformCanvasLayout(x: number, y: number, w: number, h: number)`
- `#!ts scrollpanel:PerformBarLayout(x: number, y: number, w: number, h: number)`

## Behavior
- Virtualizes child rendering by parking off-screen items at `10000,10000` and marking `pnl.b_Outside`.
- Smoothly interpolates `m_ScrollPointer` toward `m_ScrollTarget`.
- Supports both vertical and horizontal scrolling with matching bar type.
