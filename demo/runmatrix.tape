Output demo/runmatrix.gif

Set FontSize 18
Set Width 1200
Set Height 720
Set Theme "Builtin Solarized Dark"

Type "cd /Users/af/runmatrix"
Enter
Sleep 500ms

Type "uv run python -m runmatrix.cli.main plan examples/basic.yaml"
Enter
Sleep 2s

Type "clear"
Enter
Sleep 300ms

Type "uv run python -m runmatrix.cli.main run examples/basic.yaml"
Enter
Sleep 2s
