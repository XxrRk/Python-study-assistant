"""本地模块判定测试：以下导入都应视为项目内模块。"""
import os

from .utils import helper
from ..common.config import load_config
from window_capture import WindowCapture
from region_selector import RegionSelector
from gui_monitor import MonitorWindow


def run():
    helper()
    load_config()
    cap = WindowCapture(max_buffer_len=2)
    selector = RegionSelector()
    window = MonitorWindow()
    return os.path.abspath("."), cap, selector, window
