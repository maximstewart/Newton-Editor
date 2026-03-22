___
### Add
1. Add Godot LSP Client
1. Add TreeSitter
1. Add Collapsable code blocks
1. Add Terminal plugin
1. Add Plugin to <Shift\><Ctrl\>| and <Ctrl\>| to split views up, down, left, right
1. Add <Ctrl\>i to **lsp_manager** to list who implements xyz

___
### Change
1. Make **telescope** plugin a generic base to allow query mode additions through plugins
1. Make **lsp_manager** hard coded values configurable, plus add respective fields to UI

___
### Fix
- Fix on lsp client unload to close files lsp side and unload server endpoint
- Fix multi-select <Shift\><Ctrl\> left/right block select movement de-sync
       from leader when '_' in word

___
