# pathlib 复习

pathlib 用 Path 对象表示路径，`Path("data") / "file.txt"` 可以拼接路径。

`Path("data/file.txt").parent` 返回父目录 `Path("data")`。

`Path(".").glob("*.py")` 可以按通配符查找文件。
