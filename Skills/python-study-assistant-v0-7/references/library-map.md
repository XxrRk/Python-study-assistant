# 导入名 → 安装包名映射与库判定（v0.7.0）

> 机读映射见同目录的 `library-map.yaml`；本文件保留人工说明与边界规则。

本表用于把 `import` 使用的模块名映射到 pip 安装的发行版名。表里没有的名称不要猜；先确认标准库，再确认发行版，否则按“未确认导入”处理。

## 常见映射

| 导入名 | 安装包名 | 说明 |
| --- | --- | --- |
| `PIL` | `Pillow` | 历史名 PIL，发行版为 Pillow |
| `yaml` | `PyYAML` | 大小写不敏感 |
| `bs4` | `beautifulsoup4` | BeautifulSoup 的导入名 |
| `sklearn` | `scikit-learn` | 不要写成 sklearn |
| `cv2` | `opencv-python` | 可选 opencv-contrib-python |
| `dateutil` | `python-dateutil` | 不要把包名写成 dateutil |
| `dotenv` | `python-dotenv` | |
| `jwt` | `PyJWT` | 与 python-jose 不同 |
| `Crypto` | `pycryptodome` | 不是 pycrypto |
| `win32api` | `pywin32` | Windows 专用 |
| `win32com` | `pywin32` | 与 win32api 同包 |
| `serial` | `pyserial` | |
| `OpenGL` | `PyOpenGL` | |
| `skimage` | `scikit-image` | |
| `docx` | `python-docx` | |
| `pptx` | `python-pptx` | |
| `grpc` | `grpcio` | |
| `pydirectinput` | `pydirectinput` | PyPI 名称大小写不敏感 |
| `numpy` | `numpy` | 标准数值库 |
| `pandas` | `pandas` | |
| `requests` | `requests` | |
| `matplotlib` | `matplotlib` | |
| `pytest` | `pytest` | |
| `flask` | `Flask` | PyPI 名称大小写不敏感 |
| `django` | `Django` | |
| `fastapi` | `fastapi` | |
| `sqlalchemy` | `SQLAlchemy` | |
| `pymongo` | `pymongo` | |
| `redis` | `redis` | |
| `boto3` | `boto3` | |
| `cryptography` | `cryptography` | |
| `OpenSSL` | `pyOpenSSL` | 导入名与发行版不同 |
| `git` | `GitPython` | 不要与 Git 命令行混淆 |
| `pkg_resources` | `setuptools` | 旧式导入名 |
| `setuptools` | `setuptools` | 标准发行版 |

## 判定顺序

1. **先判断是否本地模块**：相对导入（`from .x import ...`）、与当前文件同目录的 `.py`/包目录、项目内明确文件。本地模块不生成库卡片，可在相关知识点卡片中说明来自项目。
2. **再判断是否标准库**：优先用 `python -c "import sys; print(name in sys.stdlib_module_names)"` 或等价方式。标准库模块 `kind=stdlib`，`package` 与导入名相同。
3. **再查上表映射**：命中则用表中的安装包名。
4. **再确认公开发行版**：材料、README、安装命令或公开信息能确认时写入真实包名。
5. **仍无法确认**：不要生成库卡片，也不要在 `package` 字段编造名称；在输出开头列出：

   ```text
   未确认导入：internal_sdk（未生成库卡片）
   ```

   若材料确实讲解了该模块的用法，可以在知识点卡片中说明其作用，但不声明安装名。

## 边界

- 导入名与发行版名大小写不敏感，pip 安装通常也不区分大小写；展示时保留官方 PyPI 名称更清晰。
- 同名不同包：如 `jwt` 可能是 PyJWT 或 python-jose 的用法，优先按材料/依赖清单确认。
- 废弃包名：如 `sklearn` 不是可安装发行版；`pycrypto` 已不再维护，优先 `pycryptodome`。
- 标准库在 Python 版本间有增删；用当前运行环境的 `sys.stdlib_module_names` 判断，不要凭记忆把第三方库当标准库。
- 多子模块只算一个库：`PyQt6.QtWidgets` 与 `PyQt6.QtCore` 同属 PyQt6；`colormath.color_objects` 与 `colormath.color_diff` 同属 colormath。
- 只出现库名、没有实际用法时，仍给出库卡片，但只写材料中能确认的定位；不要补造 API。

## 维护

- 新增映射时只添加能确认的“导入名 → PyPI 发行版名”关系；不确定就留空。
- 优先维护常见科学计算、Web、测试、打包和 Windows 生态的包名映射。
- 修改本表后，在测试材料中补充对应别名夹具，并确认库覆盖 100%、包名错误 0。
