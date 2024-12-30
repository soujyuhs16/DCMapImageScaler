from PIL import Image
import numpy as np
from typing import Tuple, List, Callable
from color_mapper import MAP_COLORS
from math import sqrt

class MinecraftMapProcessor:
    @staticmethod
    def find_nearest_color(pixel: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Find the nearest Minecraft map color for a given pixel"""
        r, g, b = pixel
        min_distance = float('inf')
        closest_color = None
        
        for color_name, color_rgb in MAP_COLORS.items():
            # Calculate Euclidean distance
            distance = sqrt(
                (r - color_rgb[0]) ** 2 +
                (g - color_rgb[1]) ** 2 +
                (b - color_rgb[2]) ** 2
            )
            
            if distance < min_distance:
                min_distance = distance
                closest_color = color_rgb
                
        return closest_color

    @staticmethod
    def create_map_preview(
        image: Image.Image,
        progress_callback: Callable[[float], None] = None
    ) -> Image.Image:
        """Convert an image to Minecraft map style with progress updates"""
        if not image:
            return None

        # Convert image to RGB mode
        rgb_image = image.convert('RGB')
        pixels = rgb_image.load()
        width, height = rgb_image.size
        total_pixels = width * height
        
        # Create new image for the map preview
        map_preview = Image.new('RGB', (width, height))
        map_pixels = map_preview.load()

        # Process each pixel
        processed_pixels = 0
        for y in range(height):
            for x in range(width):
                original_color = pixels[x, y]
                map_color = MinecraftMapProcessor.find_nearest_color(original_color)
                map_pixels[x, y] = map_color
                
                processed_pixels += 1
                if progress_callback and processed_pixels % 1000 == 0:
                    progress = (processed_pixels / total_pixels) * 100
                    progress_callback(progress)

        # Ensure 100% progress is reported
        if progress_callback:
            progress_callback(100)

        return map_preview