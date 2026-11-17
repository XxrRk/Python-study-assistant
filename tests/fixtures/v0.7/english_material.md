# pathlib essentials

`pathlib` is a Python standard library that represents filesystem paths with `Path` objects instead of plain strings.

`Path("data") / "file.txt"` joins path segments. `Path("data/file.txt").parent` returns the parent directory.

`Path(".").glob("*.py")` finds Python files in the current directory.
