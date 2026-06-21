from PIL import Image, ImageEnhance
import os

class ImageProcessor:
    def __init__(self,img_path):
        self.img_name=os.path.basename(img_path)
        self.img_path=img_path
        try:
            self.img_data = Image.open(img_path)
        except Exception as e:
            print(f"文件不存在，无法加载图片{e}")
            self.img_data = None

    def image_load(self):
        if self.img_data:
            self.img_data.show()
        else:
            print("错误：图片不存在！")
    def image_process(self):
        pass
    def image_save(self,out_path):
        self.img_data.save(out_path)

class GrayFilter(ImageProcessor):
    def image_process(self):
        self.img_data=self.img_data.convert('L')
        return self

class ResizeProcessor(ImageProcessor):
    def __init__(self,img_path,target_width,target_height):
        super().__init__(img_path)
        self.width=target_width
        self.height=target_height
    def image_process(self):
        self.img_data=self.img_data.resize((self.width,self.height))
        print(f"图片已缩放至{self.width}*{self.height}")
        return self

class BrightnessProcessor(ImageProcessor):
    def __init__(self,img_path,factor=1.0):
        super().__init__(img_path)
        self.factor=factor
    def image_process(self):
        enhancer = ImageEnhance.Brightness(self.img_data)
        self.img_data=enhancer.enhance(self.factor)
        print(f"{self.img_name}的亮度已调整，系数为{self.factor}")
        return self

class WorkflowProcessor():
    def __init__(self,img_path):
        self.img_path=img_path
        self.processors=[]
    def add_processor(self,processor_instance):
        self.processors.append(processor_instance)
        print(f"已添加步骤：{processor_instance.__class__.__name__}")
        return self
    def run_workflow(self,out_path):
        print("---开始执行任务流---")

        current_data=None

        for i,proc in enumerate(self.processors):
            if i==0:
                proc.image_process()
            else:
                proc.img_data=current_data
                proc.image_process()

            current_data=proc.img_data

        if current_data:
            current_data.save(out_path)
            print(f"任务流处理完成，图片保存至{out_path}")

if __name__ == "__main__":
    path="D:\\train_data\\3张图片_mmexport1755137661318,mm\\微信图片_20260608141405_383_22.jpg"
    test_pipeline=WorkflowProcessor(path)
    test_pipeline.add_processor(ResizeProcessor(path,1200,600))
    test_pipeline.add_processor(BrightnessProcessor(path,0.5))
    test_pipeline.run_workflow("test_output.jpg")