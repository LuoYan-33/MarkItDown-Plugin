# utils/file_detector.py
from pathlib import Path
from typing import Set

class FileDetector:
    """文件类型检测器"""

    # 可转换的文件格式
    CONVERTIBLE_FORMATS: Set[str] = {
        # 文档格式
        "pdf", "docx", "pptx", "xlsx", "xls", "epub", "rtf",
        # 网页格式
        "html", "htm",
        # 文本格式
        "csv", "json", "xml",
        # 其他格式
        "md", "rst", "asciidoc",
    }

    # 支持 OCR 的格式
    OCR_SUPPORTED_FORMATS: Set[str] = {
        "pdf", "docx", "pptx", "xlsx", "xls",
    }

    # 图片格式
    IMAGE_FORMATS: Set[str] = {
        "png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif", "webp",
    }

    def is_convertible(self, file_path: str) -> bool:
        """判断文件是否可转换"""
        ext = self._get_extension(file_path)
        return ext in self.CONVERTIBLE_FORMATS or ext in self.IMAGE_FORMATS

    def get_file_type(self, file_path: str) -> str:
        """获取文件类型"""
        return self._get_extension(file_path)

    def is_ocr_supported(self, file_path: str) -> bool:
        """判断是否支持 OCR"""
        ext = self._get_extension(file_path)
        return ext in self.OCR_SUPPORTED_FORMATS

    def is_image(self, file_path: str) -> bool:
        """判断是否为图片"""
        ext = self._get_extension(file_path)
        return ext in self.IMAGE_FORMATS

    def _get_extension(self, file_path: str) -> str:
        """获取文件扩展名"""
        return Path(file_path).suffix.lower().lstrip(".")
