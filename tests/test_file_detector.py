# tests/test_file_detector.py
import pytest
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.file_detector import FileDetector

def test_detect_by_extension():
    """测试通过扩展名检测文件类型"""
    detector = FileDetector()

    assert detector.is_convertible("test.pdf") == True
    assert detector.is_convertible("test.docx") == True
    assert detector.is_convertible("test.pptx") == True
    assert detector.is_convertible("test.xlsx") == True
    assert detector.is_convertible("test.txt") == False
    assert detector.is_convertible("test.py") == False

def test_get_file_type():
    """测试获取文件类型"""
    detector = FileDetector()

    assert detector.get_file_type("test.pdf") == "pdf"
    assert detector.get_file_type("test.docx") == "docx"
    assert detector.get_file_type("test.pptx") == "pptx"
    assert detector.get_file_type("test.xlsx") == "xlsx"

def test_is_ocr_supported():
    """测试是否支持 OCR"""
    detector = FileDetector()

    assert detector.is_ocr_supported("test.pdf") == True
    assert detector.is_ocr_supported("test.docx") == True
    assert detector.is_ocr_supported("test.pptx") == True
    assert detector.is_ocr_supported("test.xlsx") == True
    assert detector.is_ocr_supported("test.txt") == False

def test_is_image():
    """测试是否为图片"""
    detector = FileDetector()

    assert detector.is_image("test.png") == True
    assert detector.is_image("test.jpg") == True
    assert detector.is_image("test.jpeg") == True
    assert detector.is_image("test.gif") == True
    assert detector.is_image("test.bmp") == True
    assert detector.is_image("test.txt") == False
