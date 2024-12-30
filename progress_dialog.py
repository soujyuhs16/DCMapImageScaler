import tkinter as tk
from tkinter import ttk

class ProgressDialog:
    def __init__(self, parent, title="处理中", on_cancel=None):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("300x150")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Store cancel callback
        self.on_cancel = on_cancel
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        ttk.Label(self.window, text="正在生成地图画预览...").pack(pady=(10, 5))
        self.progress_bar = ttk.Progressbar(
            self.window,
            variable=self.progress_var,
            maximum=100,
            length=250,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)
        
        # Progress text
        self.progress_text = tk.StringVar(value="0%")
        ttk.Label(self.window, textvariable=self.progress_text).pack(pady=5)
        
        # Cancel button
        self.cancel_button = ttk.Button(
            self.window,
            text="取消",
            command=self._on_cancel_clicked
        )
        self.cancel_button.pack(pady=10)
        
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
        
    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        if self.on_cancel:
            self.on_cancel()
        self.close()
        
    def update_progress(self, value, text=None):
        """Update progress bar value and text"""
        self.progress_var.set(value)
        if text is None:
            text = f"{int(value)}%"
        self.progress_text.set(text)
        self.window.update()
    
    def close(self):
        """Close the progress dialog"""
        self.window.grab_release()
        self.window.destroy()