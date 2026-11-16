# pathlib 长文材料

## 1. 基础

pathlib 用 `Path` 对象表示文件路径，比直接拼接字符串更清晰。

```python
from pathlib import Path

p = Path("data") / "file.txt"
print(p)
```

## 2. 拼接路径

`Path("data") / "file.txt"` 可以拼接路径；`Path("data/file.txt").parent` 返回父目录。

```python
from pathlib import Path

print(Path("data") / "file.txt")
print(Path("data/file.txt").parent)
```

## 3. 广告

本段是广告和课程推荐，不包含 Python 知识。

## 4. 通配符

`Path(".").glob("*.py")` 会按通配符查找当前目录下的 Python 文件。

```python
from pathlib import Path

for path in Path(".").glob("*.py"):
    print(path)
```
