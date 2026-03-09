# Tree
Defines tree controls for generic nodes, local filesystem nodes, and callback-driven remote filesystem nodes.

## Classes
- `#!ts BSA.Interface.TreeNode` (base: `DTree_Node`)
- `#!ts BSA.Interface.Tree` (base: `BSA.Interface.ScrollPanel`)
- `#!ts BSA.Interface.FileTree` (base: `BSA.Interface.Tree`)
- `#!ts BSA.Interface.RemoteFileTree` (base: `BSA.Interface.FileTree`)

## TreeNode Functions
- `#!ts treenode:AddNode(name: string, icon?: string)`
- `#!ts treenode:Copy()`
- `#!ts treenode:PerformLayout()`

## Tree Functions
- `#!ts tree:Root()`
- `#!ts tree:AddNode(name: string, icon?: string)`
- `#!ts tree:Clear()`
- `#!ts tree:SetSelectedItem(node: Panel)`
- `#!ts tree:OnNodeSelected(node: Panel)`
- `#!ts tree:DoClick(node: Panel): boolean`
- `#!ts tree:DoRightClick(node: Panel): boolean`
- `#!ts tree:MoveChildTo(child: Panel, pos: number)`
- `#!ts tree:LayoutTree()`
- `#!ts tree:Setup(): boolean`
- `#!ts tree:Defer()`
- `#!ts tree:OnThink()`

## FileTree Functions
- `#!ts filetree:SetBaseFolder(base: string)`
- `#!ts filetree:SetPath(path: string)`
- `#!ts filetree:SetSearch(search: string)`
- `#!ts filetree:SetFileTypes(types: string)`
- `#!ts filetree:SetCurrentFolder(dir: string)`
- `#!ts filetree:MakeFolder(name: string, path: string, parent?: Panel)`
- `#!ts filetree:MakeFile(name: string, path: string, parent?: Panel)`
- `#!ts filetree:Setup(): boolean`
- `#!ts filetree:Defer()`
- `#!ts filetree:IsDiscovering(length?: boolean): boolean|number`
- `#!ts filetree:Discovering()`
- `#!ts filetree:OnDiscoverStart()`
- `#!ts filetree:OnDiscoverEnd()`
- `#!ts filetree:OnFileAdded(node: Panel)`
- `#!ts filetree:OnFolderAdded(node: Panel)`

## RemoteFileTree Functions
- `#!ts remotefiletree:OnFind(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:OnExists(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:OnWrite(node: Panel, name: string, path: string, data: any, callback: function)`
- `#!ts remotefiletree:OnRead(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:OnCreateDir(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:OnDelete(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:OnDiscover(node: Panel, name: string, path: string, callback: function)`
- `#!ts remotefiletree:Discover(callback?: function)`
- `#!ts remotefiletree:MakeFolder(name: string, path: string, parent?: Panel)`
- `#!ts remotefiletree:MakeFile(name: string, path: string, parent?: Panel)`

## Behavior
- Tree setup/discovery is deferred over frames via queue processing.
- `FileTree` node helpers perform direct `file.*` operations.
- `RemoteFileTree` wraps the same UX but routes file actions through overridable callbacks.
