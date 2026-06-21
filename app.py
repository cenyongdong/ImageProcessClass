import streamlit as st
from PIL import Image
# 假设你之前的类定义在 image_logic.py 中
from ImageProcessBox import ResizeProcessor, BrightnessProcessor, GrayFilter, WorkflowProcessor

st.set_page_config(page_title="AI 图像处理工作站")

st.title("🖼️ 模块化图像处理实验室")
st.write("基于面向对象思想构建的可视化流水线")


# --- 侧边栏：参数配置 ---
st.sidebar.header("第一步：上传图片")
uploaded_file = st.sidebar.file_uploader("选择一张图片...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 加载图片
    input_image = Image.open(uploaded_file)
    # 为了方便展示，我们将上传的文件临时存一下，或者修改你的类让它直接接受 PIL 对象

    st.sidebar.header("第二步：配置流水线")

    # 选项：是否开启缩放
    use_resize = st.sidebar.checkbox("开启尺寸缩放")
    target_w = st.sidebar.number_input("目标宽度", value=800) if use_resize else None
    target_h = st.sidebar.number_input("目标高度", value=600) if use_resize else None

    # 选项：亮度调整
    use_brightness = st.sidebar.checkbox("开启亮度调节")
    bright_val = st.sidebar.slider("亮度系数", 0.0, 3.0, 1.0) if use_brightness else 1.0

    # 选项：灰度
    use_gray = st.sidebar.checkbox("开启灰度滤镜")

    # --- 主界面：对比展示 ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始图片")
        st.image(input_image, use_column_width=True)

    if st.button("🚀 执行流水线处理"):
        with st.spinner('正在处理中...'):
            # --- 核心：在这里实例化你的类 ---
            # 这里的逻辑就是你之前写的 WorkflowManager 的逻辑

            # 为了演示，我们模拟一个简化的流（或者直接用你之前的类）
            # 注意：在 UI 中，由于没有真实的磁盘路径，
            # 你可能需要稍微改一下你的类，让它能直接接受 PIL 对象作为输入

            result_img = input_image

            if use_resize:
                # 假设你修改了 ResizeProcessor 让它接受 Image 对象
                result_img = result_img.resize((target_w, target_h))

            if use_brightness:
                from PIL import ImageEnhance

                enhancer = ImageEnhance.Brightness(result_img)
                result_img = enhancer.enhance(bright_val)

            if use_gray:
                result_img = result_img.convert('L')

            with col2:
                st.subheader("处理结果")
                st.image(result_img, use_column_width=True)
                st.success("流水线任务执行成功！")