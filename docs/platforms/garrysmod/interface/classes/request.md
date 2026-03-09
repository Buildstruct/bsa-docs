# Request
Provides UI request helper builders on `BSA.Interface.Request`.

## Functions
- `#!ts BSA.Interface.Request.StringClassic(title: string, text: string, defaultText: string, onEnter: function, onCancel?: function, okLabel?: string, cancelLabel?: string): BSA.Interface.Frame`
- `#!ts BSA.Interface.Request.Form(title: string, description?: string): BSA.Interface.Frame`

## Form Window Methods
- `#!ts window:OnSuccess(callback: function): self`
- `#!ts window:OnFailure(callback: function): self`
- `#!ts window:Format()`
- `#!ts window:AddString(name: string, title?: string, default?: string, placeholder?: string): self`
- `#!ts window:AddNumeric(name: string, title?: string, default?: number|string, placeholder?: string): self`

## Behavior
- `StringClassic` opens a modal frame prompt with text entry and OK/Cancel buttons.
- `Form` builds a dynamic form and returns values as `{ [name] = value }` on success/failure callbacks.

## Note
- Current implementation references `InnerPanel` in `Form` where `Container` is likely intended.
This appears to be a source bug in the Lua file rather than documentation behavior.
