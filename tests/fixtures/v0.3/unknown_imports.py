"""未知导入与本地模块测试（不执行）。"""
import os

from .local_utils import helper
from myproject.config import load_config
import internal_company_sdk


def main():
    helper()
    load_config()
    internal_company_sdk.run()
    return os.name
