"""副作用示例测试：这些函数不应被实际执行。"""
import os
import tkinter as tk

import pydirectinput
import requests


def fetch(url):
    return requests.get(url, timeout=5).text


def click():
    pydirectinput.click(100, 200)


def save_then_delete(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("data")
    os.remove(path)


def launch_gui():
    root = tk.Tk()
    root.mainloop()
