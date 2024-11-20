import tkinter as tk
from tkinter import ttk, filedialog
from image_utils import ImageProcessor

class ControlPanel(ttk.Frame):
    def __init__(self, parent, on_image_selected, on_scale_changed, on_save_clicked, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Callbacks
        self.on_image_selected = on_image_selected
        self.on_scale_changed = on_scale_changed
        self.on_save_clicked = on_save_clicked
        
        # File selection
        self.file_path = tk.StringVar()
        ttk.Label(self, text="图片文件路径:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(self, textvariable=self.file_path, width=40).pack(anchor=tk.W)
        ttk.Button(self, text="浏览...", command=self._browse_file).pack(anchor=tk.W, pady=(5, 20))
        
        # Scale controls frame
        scale_frame = ttk.LabelFrame(self, text="缩放设置", padding=(10, 5))
        scale_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Width multiple
        ttk.Label(scale_frame, text="宽 (1 = 128px):").pack(anchor=tk.W)
        self.width_multiple = ttk.Spinbox(
            scale_frame,
            from_=1,
            to=20,
            width=10,
            command=self._on_scale_change
        )
        self.width_multiple.pack(anchor=tk.W, pady=(5, 15))
        self.width_multiple.set(2)
        self.width_multiple.bind('<KeyRelease>', self._on_scale_change)
        
        # Height multiple
        ttk.Label(scale_frame, text="高 (1 = 128px):").pack(anchor=tk.W)
        self.height_multiple = ttk.Spinbox(
            scale_frame,
            from_=1,
            to=20,
            width=10,
            command=self._on_scale_change
        )
        self.height_multiple.pack(anchor=tk.W, pady=(5, 10))
        self.height_multiple.set(2)
        self.height_multiple.bind('<KeyRelease>', self._on_scale_change)
        
        # Price display
        self.price_var = tk.StringVar()
        self.price_var.set("生成地图画将需要花费: 100 DCB")
        ttk.Label(scale_frame, textvariable=self.price_var, font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(
            button_frame,
            text="更新预览图",
            command=self._on_scale_change
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="另存为图片",
            command=self.on_save_clicked
        ).pack(side=tk.LEFT)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(
            self,
            textvariable=self.status_var,
            wraplength=350
        ).pack(anchor=tk.W, pady=(20, 0))
        
        # Initial price calculation
        self._update_price()
    
    def update_filepath(self, file_path: str):
        self.file_path.set(file_path)

    def _browse_file(self):
        """Handle file browse button click"""
        filetypes = (
            ('图片文件', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('所有文件', '*.*')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            self.on_image_selected(filename)
    
    def _on_scale_change(self, event = None):
        """Handle scale value changes"""
        try:
            width = int(self.width_multiple.get())
            height = int(self.height_multiple.get())
            self._update_price()
            self.on_scale_changed(width, height)
        except ValueError:
            pass
    
    def _update_price(self):
        """Update the price display"""
        try:
            width = int(self.width_multiple.get())
            height = int(self.height_multiple.get())
            price = ImageProcessor.calculate_price(width, height)
            self.price_var.set(f"生成地图画将需要花费: {price} DCB")
        except ValueError:
            self.price_var.set("Invalid input")
    
    def set_status(self, message):
        """Update status message"""
        self.status_var.set(message)