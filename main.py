import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinterdnd2 as tkdnd
from PIL import Image
import os

from image_utils import ImageProcessor
from minecraft_map_processor import MinecraftMapProcessor
from preview_canvas import PreviewCanvas
from control_panel import ControlPanel
from progress_dialog import ProgressDialog
from threaded_processor import ThreadedProcessor

class ImageScalerApp:
    def __init__(self, root: tkdnd.Tk):
        self.root = root
        self.root.title("DC服务器地图画缩放器")
        self.root.geometry("1024x768")

        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drag_drop)

        # Configure main window scaling
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Create control panel
        self.control_panel = ControlPanel(
            main_frame,
            on_image_selected=self.load_image,
            on_scale_changed=self.update_preview,
            on_save_clicked=self.save_image,
            on_preview_mode_changed=self.change_preview_mode
        )
        self.control_panel.grid(row=0, column=0, sticky="nw", padx=(0, 20))

        # Create preview canvas
        self.preview_canvas = PreviewCanvas(main_frame)
        self.preview_canvas.grid(row=0, column=1, sticky="nsew")

        # Initialize variables
        self.original_image = None
        self.scaled_image = None
        self.preview_mode = "normal"
        
        # Initialize threaded processor
        self.processor = ThreadedProcessor(self.on_processing_complete)
        
        # Schedule periodic updates
        self.root.after(100, self.check_processing)

    def check_processing(self):
        """Check for completed processing tasks"""
        self.processor.update()
        self.root.after(100, self.check_processing)

    def change_preview_mode(self, mode):
        """Change the preview mode between normal and minecraft"""
        self.preview_mode = mode
        self.preview_canvas.set_preview_mode(mode)
        self.update_preview()

    def on_drag_drop(self, event):
        file_path = event.data
        self.control_panel.update_filepath(file_path)
        self.load_image(file_path)

    def load_image(self, file_path):
        """Load and display the selected image"""
        try:
            self.original_image = Image.open(file_path)
            self.control_panel.set_status("图片加载成功")
            self.update_preview()
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
            self.original_image = None

    def cancel_preview(self):
        """Cancel the current preview processing"""
        self.processor.cancel()
        self.preview_mode = "normal"
        self.control_panel.preview_mode.set("normal")
        self.preview_canvas.set_preview_mode("normal")
        self.update_preview()

    def update_preview(self, width_multiple=None, height_multiple=None):
        """Update the preview with current scale settings"""
        if not self.original_image:
            return

        try:
            # Get current scale values if not provided
            if width_multiple is None:
                width_multiple = int(self.control_panel.width_multiple.get())
            if height_multiple is None:
                height_multiple = int(self.control_panel.height_multiple.get())

            # Validate scale values
            if width_multiple <= 0 or height_multiple <= 0:
                messagebox.showerror("错误", "倍数必须是正整数")
                return

            # Scale image
            self.scaled_image = ImageProcessor.scale_image(
                self.original_image,
                width_multiple,
                height_multiple
            )

            # Create preview based on mode
            if self.preview_mode == "minecraft":
                # Show progress dialog and process in thread
                self.progress_dialog = ProgressDialog(
                    self.root,
                    on_cancel=self.cancel_preview
                )
                self.processor.process(
                    MinecraftMapProcessor.create_map_preview,
                    self.scaled_image,
                    self.progress_dialog.update_progress
                )
            else:
                # Normal preview
                preview = ImageProcessor.create_preview(
                    self.scaled_image,
                    self.preview_canvas.canvas.winfo_width(),
                    self.preview_canvas.canvas.winfo_height()
                )
                self.preview_canvas.update_preview(preview)

            # Calculate price
            price = ImageProcessor.calculate_price(width_multiple, height_multiple)

            # Update status
            self.control_panel.set_status(
                f"图片像素: {self.scaled_image.width}x{self.scaled_image.height} pixels (生成地图画将需要花费: {price} DCB)"
            )

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_processing_complete(self, success, result):
        """Handle completion of threaded processing"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
            delattr(self, 'progress_dialog')

        if success:
            preview = ImageProcessor.create_preview(
                result,
                self.preview_canvas.canvas.winfo_width(),
                self.preview_canvas.canvas.winfo_height()
            )
            self.preview_canvas.update_preview(preview)
        else:
            messagebox.showerror("错误", f"处理失败: {result}")

    def save_image(self):
        """Save the scaled image"""
        if not self.scaled_image:
            messagebox.showerror("错误", "您还没有加载图片呢")
            return

        try:
            # Ask for save location
            file_types = [
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg'),
                ('All files', '*.*')
            ]
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=file_types,
                initialfile=f"scaled_{self.scaled_image.width}x{self.scaled_image.height}"
            )

            if save_path:
                # Always save the scaled image, not the minecraft preview
                self.scaled_image.save(save_path)

                # Calculate final price
                width_multiple = self.scaled_image.width // 128
                height_multiple = self.scaled_image.height // 128
                price = ImageProcessor.calculate_price(width_multiple, height_multiple)

                self.control_panel.set_status(
                    f"图片另存为: {os.path.basename(save_path)} (生成地图画将需要花费: {price} DCB)"
                )

        except Exception as e:
            messagebox.showerror("错误", f"保存图片失败: {str(e)}")


def main():
    root = tkdnd.Tk()
    ImageScalerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()