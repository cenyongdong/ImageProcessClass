import streamlit as st
from PIL import Image
import io
from ImageProcessBox import (
    ResizeProcessor, 
    BrightnessProcessor, 
    GrayFilter, 
    ContrastProcessor,
    SaturationProcessor,
    BlurProcessor,
    WorkflowProcessor
)

# Page configuration
st.set_page_config(
    page_title="Image Processing Studio",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 20px;
    }
    .section-header {
        color: #ff7f0e;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-header'>🖼️ Modular Image Processing Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>An OOP-based visual image processing pipeline</p>", unsafe_allow_html=True)

# ===== SIDEBAR: Image Upload and Pipeline Configuration =====
st.sidebar.markdown("### 📸 Step 1: Upload Image")
uploaded_file = st.sidebar.file_uploader(
    "Choose an image file", 
    type=["jpg", "jpeg", "png", "bmp", "gif"],
    help="Supported formats: JPG, PNG, BMP, GIF"
)

if uploaded_file:
    # Load the uploaded image
    input_image = Image.open(uploaded_file)
    
    st.sidebar.markdown("### ⚙️ Step 2: Configure Pipeline")
    
    # Show original image dimensions
    img_width, img_height = input_image.size
    st.sidebar.info(f"📐 Original size: {img_width} × {img_height} px")
    
    # ===== RESIZE OPTIONS =====
    st.sidebar.markdown("#### 📏 Resize")
    use_resize = st.sidebar.checkbox("Enable Resize", key="resize_check")
    if use_resize:
        resize_mode = st.sidebar.radio(
            "Resize Mode",
            ["Custom", "Preset"],
            key="resize_mode"
        )
        
        if resize_mode == "Custom":
            col_w, col_h = st.sidebar.columns(2)
            with col_w:
                target_w = st.number_input("Width (px)", value=img_width, min_value=50, step=50)
            with col_h:
                target_h = st.number_input("Height (px)", value=img_height, min_value=50, step=50)
        else:
            preset = st.sidebar.selectbox(
                "Choose preset",
                ["800x600", "1024x768", "1200x800", "640x480"]
            )
            target_w, target_h = map(int, preset.split("x"))
    
    # ===== BRIGHTNESS OPTIONS =====
    st.sidebar.markdown("#### ☀️ Brightness")
    use_brightness = st.sidebar.checkbox("Enable Brightness", key="brightness_check")
    if use_brightness:
        brightness_factor = st.sidebar.slider(
            "Brightness Factor",
            min_value=0.0,
            max_value=3.0,
            value=1.0,
            step=0.1,
            help="< 1.0 = darker, > 1.0 = brighter"
        )
    
    # ===== CONTRAST OPTIONS =====
    st.sidebar.markdown("#### 🎨 Contrast")
    use_contrast = st.sidebar.checkbox("Enable Contrast", key="contrast_check")
    if use_contrast:
        contrast_factor = st.sidebar.slider(
            "Contrast Factor",
            min_value=0.0,
            max_value=3.0,
            value=1.0,
            step=0.1,
            help="< 1.0 = lower contrast, > 1.0 = higher contrast"
        )
    
    # ===== SATURATION OPTIONS =====
    st.sidebar.markdown("#### 🌈 Saturation")
    use_saturation = st.sidebar.checkbox("Enable Saturation", key="saturation_check")
    if use_saturation:
        saturation_factor = st.sidebar.slider(
            "Saturation Factor",
            min_value=0.0,
            max_value=2.5,
            value=1.0,
            step=0.1,
            help="0 = grayscale, 1 = normal, > 1 = more vivid"
        )
    
    # ===== BLUR OPTIONS =====
    st.sidebar.markdown("#### 🌫️ Blur")
    use_blur = st.sidebar.checkbox("Enable Blur", key="blur_check")
    if use_blur:
        blur_radius = st.sidebar.slider(
            "Blur Radius",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
            help="Higher value = more blur"
        )
    
    # ===== GRAYSCALE OPTION =====
    st.sidebar.markdown("#### ⚫ Filters")
    use_grayscale = st.sidebar.checkbox("Enable Grayscale", key="grayscale_check")
    
    # ===== MAIN DISPLAY AREA =====
    st.markdown("### 🔄 Processing Pipeline")
    
    # Display original and result side by side
    col_original, col_result = st.columns(2)
    
    with col_original:
        st.markdown("#### Original Image")
        st.image(input_image, use_column_width=True)
    
    # Process button
    if st.button("🚀 Execute Pipeline", key="execute_btn", use_container_width=True):
        with st.spinner("Processing your image..."):
            try:
                # Create workflow with the uploaded image
                workflow = WorkflowProcessor(input_image)
                
                # Add processors based on user selections
                if use_resize:
                    workflow.add_processor(
                        ResizeProcessor(input_image, target_w, target_h)
                    )
                
                if use_brightness:
                    workflow.add_processor(
                        BrightnessProcessor(input_image, brightness_factor)
                    )
                
                if use_contrast:
                    workflow.add_processor(
                        ContrastProcessor(input_image, contrast_factor)
                    )
                
                if use_saturation:
                    workflow.add_processor(
                        SaturationProcessor(input_image, saturation_factor)
                    )
                
                if use_blur:
                    workflow.add_processor(
                        BlurProcessor(input_image, blur_radius)
                    )
                
                if use_grayscale:
                    workflow.add_processor(GrayFilter(input_image))
                
                # Execute the workflow
                result_image = workflow.run_workflow()
                
                # Display result
                with col_result:
                    st.markdown("#### Processed Image")
                    st.image(result_image, use_column_width=True)
                
                # Download button
                st.markdown("### 📥 Download Result")
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                buf.seek(0)
                
                st.download_button(
                    label="⬇️ Download Processed Image",
                    data=buf.getvalue(),
                    file_name="processed_image.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                st.success("✅ Pipeline executed successfully!")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    # Display pipeline configuration summary
    with st.expander("📋 Pipeline Configuration Summary"):
        config_text = "**Active Processing Steps:**\n\n"
        steps = []
        if use_resize:
            steps.append(f"• Resize to {target_w}×{target_h} px")
        if use_brightness:
            steps.append(f"• Adjust brightness (factor: {brightness_factor})")
        if use_contrast:
            steps.append(f"• Adjust contrast (factor: {contrast_factor})")
        if use_saturation:
            steps.append(f"• Adjust saturation (factor: {saturation_factor})")
        if use_blur:
            steps.append(f"• Apply Gaussian blur (radius: {blur_radius})")
        if use_grayscale:
            steps.append("• Convert to grayscale")
        
        if steps:
            config_text += "\n".join(steps)
        else:
            config_text += "No processing steps selected"
        
        st.markdown(config_text)

else:
    # Show welcome message when no image is uploaded
    st.info("👈 Upload an image from the sidebar to get started!")
    
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        This image processing studio uses **Object-Oriented Programming (OOP)** 
        principles to create a flexible, modular image processing pipeline.
        
        **Features:**
        - 🔄 Chain multiple processing operations
        - 📏 Resize images to custom or preset dimensions
        - ☀️ Adjust brightness, contrast, and saturation
        - 🌫️ Apply blur effects
        - ⚫ Convert to grayscale
        - 📥 Download processed results
        
        **Built with:**
        - Streamlit (UI framework)
        - PIL/Pillow (image processing)
        - Python OOP principles
        """)
