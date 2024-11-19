from PIL import Image, ImageTk
import tkinter as tk

class ImageProcessor:
    @staticmethod
    def scale_image(image, width_multiple, height_multiple):
        """Scale image to multiples of 128 pixels"""
        new_width = 128 * width_multiple
        new_height = 128 * height_multiple
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def create_preview(image, canvas_width, canvas_height):
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