# Context Menu
Provides BSA-themed Derma menu helpers and menu controls.

## Globals
- `#!ts BSA.Interface.DermaMenu(parentmenu?: boolean, parent?: Panel): BSA.Interface.Menu`
- `#!ts BSA.Interface.IsDermaMenuActive(): boolean`

## Classes
- `#!ts BSA.Interface.MenuOption` (base: `BSA.Interface.Button`)
- `#!ts BSA.Interface.MenuOptionCVar` (base: `BSA.Interface.MenuOption`)
- `#!ts BSA.Interface.Menu` (base: `BSA.Interface.ScrollPanel`)

## MenuOption Functions
- `#!ts menuoption:SetSubMenu(menu: Panel)`
- `#!ts menuoption:GetSubMenu(): Panel?`
- `#!ts menuoption:AddSubMenu(): Panel`
- `#!ts menuoption:ToggleCheck()`
- `#!ts menuoption:SetChecked(state: boolean)`
- `#!ts menuoption:OnChecked(state: boolean)`
- `#!ts menuoption:DoClickInternal()`
- `#!ts menuoption:DoRightClick()`
- `#!ts menuoption:OnCursorEntered()`
- `#!ts menuoption:OnCursorExited()`

## MenuOptionCVar Functions
- `#!ts menuoptioncvar:SetConVar(name: string)`
- `#!ts menuoptioncvar:SetValueOn(value: string)`
- `#!ts menuoptioncvar:SetValueOff(value: string)`
- `#!ts menuoptioncvar:Think()`
- `#!ts menuoptioncvar:OnChecked(state: boolean)`

## Menu Functions
- `#!ts menu:AddMessage(name: string, ...: any)`
- `#!ts menu:AddCustom(panel: Panel)`
- `#!ts menu:AddOption(text: string, callback?: function)`
- `#!ts menu:AddCVar(text: string, convar: string, on: string, off: string, callback?: function)`
- `#!ts menu:AddSpacer()`
- `#!ts menu:AddSubMenu(text: string, callback?: function): Panel, Panel`
- `#!ts menu:Hide()`
- `#!ts menu:OpenSubMenu(item: Panel, menu: Panel)`
- `#!ts menu:CloseSubMenu(menu: Panel)`
- `#!ts menu:ChildCount(): number`
- `#!ts menu:GetChild(index: number): Panel?`
- `#!ts menu:LayoutReset()`
- `#!ts menu:Open(x?: number, y?: number, skipanimation?: boolean, ownerpanel?: Panel)`
- `#!ts menu:OptionSelectedInternal(option: Panel)`
- `#!ts menu:OptionSelected(option: Panel, text: string)`
- `#!ts menu:ClearHighlights()`
- `#!ts menu:HighlightItem(item: Panel)`

## Behavior
- Menus are registered with `RegisterDermaMenuForClose`.
- Submenu positioning changes slightly between root menus and submenus.
- Visuals are themed through `theme:fetch("context", ...)`.
