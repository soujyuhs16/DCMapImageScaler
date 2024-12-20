import os
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, messagebox, filedialog

import tkinterdnd2 as tkdnd
from PIL import Image

from image_utils import ImageProcessor
from preview_canvas import PreviewCanvas
from control_panel import ControlPanel


class ImageScalerApp:
    def __init__(self, root: tkdnd.Tk):
        self.root = root
        self.root.title("DC服务器地图画缩放器")
        self.root.geometry("1024x768")

        self.disabled = False
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
            on_scale_changed=self.submit_preview_task,
            on_save_clicked=self.save_image
        )
        self.control_panel.grid(row=0, column=0, sticky="nw", padx=(0, 20))

        # Create preview canvas
        self.preview_canvas = PreviewCanvas(main_frame)
        self.preview_canvas.grid(row=0, column=1, sticky="nsew")

        # Initialize image variables
        self.original_image = None
        self.scaled_image = None
        self.preview_image = None

        self.preview_task_executor = ThreadPoolExecutor(1, 'preview-task')

    def on_drag_drop(self, event):
        if self.disabled:
            return
        
        file_path = event.data
        self.control_panel.update_filepath(file_path)
        self.load_image(file_path)

    def load_image(self, file_path):
        """Load and display the selected image"""
        try:
            self.original_image = Image.open(file_path)
            self.control_panel.set_status("图片加载成功")
            self.submit_preview_task(None, None, self.control_panel.preview_option.get())
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
            self.original_image = None

    def task_execute(self, width_multiple, height_multiple):
        progress_generator = ImageProcessor.floyd_steinberg(self.scaled_image)

        self.control_panel.progress.pack()
        try:
            while True:
                progress = next(progress_generator)
                self.control_panel.progress_value.set(progress)
        except StopIteration as e:
            self.preview_image = e.value
            self.control_panel.progress.pack_forget()

        self.update_preview(width_multiple, height_multiple)
        self.disable(False)

    def disable(self, freeze: bool):
        self.disabled = freeze
        self.control_panel.disable(freeze)

    def submit_preview_task(self, width_multiple=None, height_multiple=None, preview_option='SCALE'):
        if not self.original_image:
            return
        
        # Get current scale values if not provided
        if width_multiple is None:
            width_multiple = int(self.control_panel.width_multiple.get())
        if height_multiple is None:
            height_multiple = int(self.control_panel.height_multiple.get())

        # Validate scale values
        if width_multiple <= 0 or height_multiple <= 0:
            messagebox.showerror("错误", "倍数必须是正整数")
            return
        
		# 冻结 GUI
        self.disable(True)

        # Scale image
        self.scaled_image = ImageProcessor.scale_image(
            self.original_image,
            width_multiple,
            height_multiple
        )

        if preview_option == 'SCALE':
            self.preview_image = self.scaled_image
            self.update_preview(width_multiple, height_multiple)
            self.disable(False)
            return

        # 提交任务
        self.preview_task_executor.submit(
            self.task_execute,
            width_multiple, height_multiple
        )

    def update_preview(self, width_multiple, height_multiple):
        # Create and update preview
        preview = ImageProcessor.create_preview(
            self.preview_image,
            self.preview_canvas.canvas.winfo_width(),
            self.preview_canvas.canvas.winfo_height()
        )
        self.preview_canvas.update_preview(preview)

        # Calculate price
        price = ImageProcessor.calculate_price(width_multiple, height_multiple)

        # Update status
        self.control_panel.set_status(
            f"图片像素: {self.preview_image.width}x{self.preview_image.height} pixels (生成地图画将需要花费: {price} DCB)"
        )

    def save_image(self):
        """Save the scaled image"""
        if not self.scaled_image:
            messagebox.showerror("错误", "您还没有加载图片呢")
            return

        try:
            # Ask for save location
            file_types = [
                ('PNG 文件', '*.png'),
                ('JPEG 文件', '*.jpg'),
                ('All 文件', '*.*')
            ]
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=file_types,
                initialfile=f"scaled_{self.scaled_image.width}x{self.scaled_image.height}"
            )

            if save_path:
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
