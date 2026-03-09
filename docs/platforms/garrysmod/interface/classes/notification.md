# Notification
Defines per-entry notification widgets and the notification stack manager.

## Classes
- `#!ts BSA.Interface.NotificationEntry` (base: `BSA.Interface.Label`)
- `#!ts BSA.Interface.Notification` (base: `DPanel`)

## NotificationEntry Functions
- `#!ts notificationentry:SetText(...: any): self`
- `#!ts notificationentry:OnEnded(callback: function): self`
- `#!ts notificationentry:SetProgress(state: boolean): self`
- `#!ts notificationentry:SetAwait(state: boolean): self`
- `#!ts notificationentry:SetDuration(duration?: number, absolute?: boolean): self`
- `#!ts notificationentry:GetDuration(): number`
- `#!ts notificationentry:Close()`
- `#!ts notificationentry:SizeToContents()`

## Notification Functions
- `#!ts notification:IsExternal(): boolean`
- `#!ts notification:Externalize(panel: Panel, external: boolean)`
- `#!ts notification:SetSpacing(spacing: number)`
- `#!ts notification:GetSpacing(): number`
- `#!ts notification:SetPadding(padding: number)`
- `#!ts notification:GetPadding(): number`
- `#!ts notification:Setup(panel: Panel)`
- `#!ts notification:Index(panel: Panel): number|false`
- `#!ts notification:Add(): Panel`
- `#!ts notification:Add(panel: Panel)`
- `#!ts notification:Insert(index: number, panel: Panel)`
- `#!ts notification:Move(panel: Panel, index: number)`
- `#!ts notification:GetChildren(absolute?: boolean): Panel[]`
- `#!ts notification:Clear(force?: boolean)`

## Behavior
- Entries animate in/out and are removed when `m_nEnd` is reached.
- `SetAwait(true)` shows animated activity line; `SetProgress(true)` shows time-fraction bar.
- External mode detaches stack to screen space (used when parent frame is minimized).
- Default alignment is bottom-left (`m_Alignment = "bl"`).
