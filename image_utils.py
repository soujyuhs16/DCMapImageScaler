from typing import Generator

import numpy as np
from PIL import Image

class ImageProcessor:
    @staticmethod
    def scale_image(image: Image.Image, width_multiple, height_multiple):
        """Scale image to multiples of 128 pixels"""
        new_width = 128 * width_multiple
        new_height = 128 * height_multiple
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def create_preview(image: Image.Image, canvas_width, canvas_height):
        """Create a preview that fits the canvas while maintaining aspect ratio"""
        if not image:
            return None
            
        # Calculate scaling factor
        width_ratio = canvas_width / image.width
        height_ratio = canvas_height / image.height
        scale_factor = min(width_ratio, height_ratio, 1.0)
        
        preview_width = int(image.width * scale_factor)
        preview_height = int(image.height * scale_factor)
        
        return image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def calculate_price(width_multiple, height_multiple):
        """Calculate price based on multiples"""
        return width_multiple * height_multiple * 50

    @staticmethod
    def floyd_steinberg(img: Image.Image) -> Generator[int, None, Image.Image]:
        """弗洛伊德斯坦伯格图像抖动算法"""

        # 将图像转换成 ndarray
        pixels = np.array(img, np.float32)
        rows, cols, _ = pixels.shape

        for y in range(rows - 1):
            yield int((y / rows) * 100)
            for x in range(cols - 1):
                # 量化像素
                old_px = np.array(pixels[y, x])
                new_px = np.where(old_px < 128, 0, 255)
                pixels[y, x] = new_px

                # 计算误差
                quant_error = old_px - new_px

                # 扩散误差
                pixels[y, x+1] += quant_error * (7/16)
                pixels[y+1, x-1] += quant_error * (3/16)
                pixels[y+1, x] += quant_error * (5/16)
                pixels[y+1, x+1] += quant_error * (1/16)
        
        return Image.fromarray(
            np.clip(pixels, 0, 255).astype(np.uint8)
        )