"""别名导入与包名映射测试。"""
from PIL import Image
import yaml
from bs4 import BeautifulSoup
from sklearn.linear_model import LogisticRegression
import cv2


def load(path):
    image = Image.open(path)
    with open("config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    soup = BeautifulSoup("<h1>hi</h1>", "html.parser")
    model = LogisticRegression()
    gray = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
    return image, config, soup, model, gray
