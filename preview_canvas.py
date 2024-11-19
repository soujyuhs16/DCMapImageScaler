import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

class PreviewCanvas(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create canvas with gray background
        self.canvas = tk.Canvas(
            self,
            bg='#f0f0f0',
            highlightthickness=1,
            highlightbackground='#cccccc'
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind resize event
        self.canvas.bind('<Configure>', self.on_resize)
        
        self.photo_image = None
        self.current_preview = None
    
    def update_preview(self, preview_image):
        """Update the preview with a new image"""
        if not preview_image:
            return
            
        # Store current preview
        self.current_preview = preview_image
        
        # Create PhotoImage and keep reference
        self.photo_image = ImageTk.PhotoImage(preview_image)
        
        # Clear canvas and draw new image
        self.canvas.delete("all")
        
        # Center image
        x = (self.canvas.winfo_width() - preview_image.width) // 2
        y = (self.canvas.winfo_height() - preview_image.height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)
    
    def on_resize(self, event):
        """Handle canvas resize events"""
        if self.current_preview:
            self.update_preview(self.current_preview)