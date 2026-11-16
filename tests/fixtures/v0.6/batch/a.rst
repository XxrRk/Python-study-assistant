pathlib 路径操作
================

pathlib 用 ``Path`` 对象表示文件路径，比直接拼接字符串更清晰。

.. code-block:: python

   from pathlib import Path

   p = Path("data") / "file.txt"
   print(p)

Path.parent
-----------

``Path("data/file.txt").parent`` 返回父目录 ``Path("data")``。

.. code-block:: python

   from pathlib import Path

   print(Path("data/file.txt").parent)
