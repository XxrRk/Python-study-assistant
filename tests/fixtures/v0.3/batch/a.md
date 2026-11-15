# pathlib 基础

pathlib 用 `Path` 对象表示文件路径，比字符串拼接更清晰。

`Path("data") / "file.txt"` 可以拼接路径；`Path("data/file.txt").parent` 返回父目录。
