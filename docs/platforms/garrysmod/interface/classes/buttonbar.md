# ButtonBar
`BSA.Interface.ButtonBar` is a horizontal button strip backed by `BSA.Interface.ScrollPanel`.

## Functions
- `#!ts buttonbar:AddSpacer(): Panel`
- `#!ts buttonbar:Add(name: string, callback?: function)`
- `#!ts buttonbar:AddPanel(panel: Panel): Panel`
- `#!ts buttonbar:GetLength(): number`
- `#!ts buttonbar:Paint(w: number, h: number)`
- `#!ts buttonbar:PerformLayout()`
- `#!ts buttonbar:Perform()`

## Behavior
- Uses an internal horizontal scroll panel with hidden scrollbar.
- `Add` creates `BSA.Interface.Button` entries and binds `OnMousePressed` to the callback.
- `GetLength` proxies to the internal scroll panel aggregate length.
