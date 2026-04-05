___
### Add
1. Add Godot LSP Client
1. Add Terminal plugin
1. Add <Ctrl\>i to **lsp_manager** to list who implements xyz

___
### Change
1. Make **telescope** plugin a generic base to allow query mode additions through plugins
1. Make **lsp_manager** hard coded values configurable, plus add respective fields to UI

___
### Fix
- Fix <Ctrl\>z in multi-insert mode being funky. Insure updates happen on block level.
       I.E, maybe push updates to queue to insure block undo/redo?
- Fix on lsp client unload to close files lsp side and unload server endpoint

___
