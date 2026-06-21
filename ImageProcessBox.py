from PIL import Image, ImageEnhance, ImageFilter
import os
from typing import Union

class ImageProcessor:
    """Base class for image processing with support for both file paths and PIL Image objects"""
    
    def __init__(self, img_input: Union[str, Image.Image]):
        """
        Initialize with either a file path or a PIL Image object
        
        Args:
            img_input: Either a file path (str) or a PIL Image object
        """
        if isinstance(img_input, Image.Image):
            self.img_name = "uploaded_image"
            self.img_path = None
            self.img_data = img_input
        elif isinstance(img_input, str):
            self.img_name = os.path.basename(img_input)
            self.img_path = img_input
            try:
                self.img_data = Image.open(img_input)
            except Exception as e:
                print(f"文件不存在，无法加载图片: {e}")
                self.img_data = None
        else:
            raise TypeError("img_input must be either a file path (str) or PIL Image object")

    def image_load(self):
        """Display the image"""
        if self.img_data:
            self.img_data.show()
        else:
            print("错误：图片不存在！")
    
    def image_process(self):
        """Override in subclasses to define processing logic"""
        pass
    
    def image_save(self, out_path: str):
        """Save the processed image"""
        if self.img_data:
            self.img_data.save(out_path)
            print(f"图片已保存至: {out_path}")
        else:
            print("错误：没有图片可以保存")
    
    def get_image(self) -> Image.Image:
        """Return the PIL Image object for use in web apps"""
        return self.img_data


class GrayFilter(ImageProcessor):
    """Convert image to grayscale"""
    
    def image_process(self):
        if self.img_data:
            self.img_data = self.img_data.convert('L')
        return self


class ResizeProcessor(ImageProcessor):
    """Resize image to specified dimensions"""
    
    def __init__(self, img_input: Union[str, Image.Image], target_width: int, target_height: int):
        super().__init__(img_input)
        self.width = target_width
        self.height = target_height
    
    def image_process(self):
        if self.img_data:
            self.img_data = self.img_data.resize((self.width, self.height), Image.Resampling.LANCZOS)
            print(f"图片已缩放至 {self.width}x{self.height}")
        return self


class BrightnessProcessor(ImageProcessor):
    """Adjust image brightness"""
    
    def __init__(self, img_input: Union[str, Image.Image], factor: float = 1.0):
        super().__init__(img_input)
        self.factor = factor
    
    def image_process(self):
        if self.img_data:
            enhancer = ImageEnhance.Brightness(self.img_data)
            self.img_data = enhancer.enhance(self.factor)
            print(f"{self.img_name} 的亮度已调整，系数为 {self.factor}")
        return self


class ContrastProcessor(ImageProcessor):
    """Adjust image contrast"""
    
    def __init__(self, img_input: Union[str, Image.Image], factor: float = 1.0):
        super().__init__(img_input)
        self.factor = factor
    
    def image_process(self):
        if self.img_data:
            enhancer = ImageEnhance.Contrast(self.img_data)
            self.img_data = enhancer.enhance(self.factor)
            print(f"{self.img_name} 的对比度已调整，系数为 {self.factor}")
        return self


class SaturationProcessor(ImageProcessor):
    """Adjust image color saturation"""
    
    def __init__(self, img_input: Union[str, Image.Image], factor: float = 1.0):
        super().__init__(img_input)
        self.factor = factor
    
    def image_process(self):
        if self.img_data:
            enhancer = ImageEnhance.Color(self.img_data)
            self.img_data = enhancer.enhance(self.factor)
            print(f"{self.img_name} 的饱和度已调整，系数为 {self.factor}")
        return self


class BlurProcessor(ImageProcessor):
    """Apply blur filter"""
    
    def __init__(self, img_input: Union[str, Image.Image], radius: int = 2):
        super().__init__(img_input)
        self.radius = radius
    
    def image_process(self):
        if self.img_data:
            self.img_data = self.img_data.filter(ImageFilter.GaussianBlur(radius=self.radius))
            print(f"{self.img_name} 已应用高斯模糊，半径为 {self.radius}")
        return self


class WorkflowProcessor:
    """Pipeline for chaining multiple image processors"""
    
    def __init__(self, img_input: Union[str, Image.Image]):
        """
        Initialize with either a file path or PIL Image object
        
        Args:
            img_input: Either a file path (str) or a PIL Image object
        """
        self.img_input = img_input
        self.processors = []
    
    def add_processor(self, processor_instance: ImageProcessor):
        """Add a processor to the pipeline"""
        self.processors.append(processor_instance)
        print(f"已添加处理步骤：{processor_instance.__class__.__name__}")
        return self
    
    def run_workflow(self, out_path: str = None) -> Image.Image:
        """
        Execute the workflow pipeline
        
        Args:
            out_path: Optional file path to save the result
            
        Returns:
            The processed PIL Image object
        """
        print("---开始执行任务流---")
        
        current_data = None
        
        for i, proc in enumerate(self.processors):
            if i == 0:
                # First processor uses the original image input
                if not hasattr(proc, 'img_data') or proc.img_data is None:
                    proc.__init__(self.img_input, *self._get_processor_args(proc))
                proc.image_process()
            else:
                # Subsequent processors use the output from previous step
                proc.img_data = current_data
                proc.image_process()
            
            current_data = proc.img_data
        
        if current_data and out_path:
            current_data.save(out_path)
            print(f"任务流处理完成，图片保存至 {out_path}")
        
        print("---任务流执行完成---")
        return current_data
    
    def _get_processor_args(self, proc):
        """Extract initialization arguments from processor (helper method)"""
        args = []
        if hasattr(proc, 'width') and hasattr(proc, 'height'):
            args = [proc.width, proc.height]
        elif hasattr(proc, 'factor'):
            args = [proc.factor]
        elif hasattr(proc, 'radius'):
            args = [proc.radius]
        return args


if __name__ == "__main__":
    # Example usage
    path = "test_image.jpg"  # Replace with actual image path
    
    # Create workflow
    test_pipeline = WorkflowProcessor(path)
    test_pipeline.add_processor(ResizeProcessor(path, 1200, 600))
    test_pipeline.add_processor(BrightnessProcessor(path, 0.8))
    test_pipeline.add_processor(GrayFilter(path))
    
    # Run and save
    result = test_pipeline.run_workflow("test_output.jpg")
