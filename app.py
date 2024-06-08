import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_image(image_file):
    img = Image.open(image_file)
    return img

def get_palette(image, n_colors=5):
    # Convert image to numpy array
    img_array = np.array(image)
    img_array = img_array.reshape((-1, 3))

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(img_array)
    colors = kmeans.cluster_centers_.astype(int)

    return colors

def plot_palette(colors):
    # Create a plot for the palette
    plt.figure(figsize=(8, 2))
    plt.axis('off')

    # Create a palette image
    palette = np.zeros((50, 300, 3), dtype=int)
    steps = 300 // len(colors)

    for i, color in enumerate(colors):
        palette[:, i*steps:(i+1)*steps, :] = color

    plt.imshow(palette)
    return plt

# Streamlit app setup
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Color Palette Generator"])

# Add custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        margin-top: 20px;
    }
    .content-text {
        font-size: 18px;
        color: #555;
        text-align: justify;
        margin: 20px;
    }
    .sub-header {
        font-size: 24px;
        color: #4CAF50;
        text-align: center;
        margin-top: 20px;
    }
    .color-box {
        width: 50px;
        height: 50px;
        border-radius: 5px;
        margin: 0 auto;
    }
    .color-container {
        display: flex;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 10px;
        justify-items: center;
        align-items: center;
    }
    .color-item {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if app_mode == "Home":
    st.markdown('<div class="main-header">DOMINANT COLOR PALETTE GENERATOR</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="content-text">
            Welcome to the Dominant Color Palette Generator! This application allows you to upload an image and generate a color palette based on the most dominant colors in the image. Use the sidebar to navigate between the home page, learn more about the project, or start generating your color palette.
        </div>
    """, unsafe_allow_html=True)
    image_path = "home_img.jpeg"
    st.image(image_path, use_column_width=True)

elif app_mode == "About Project":
    st.markdown('<div class="main-header">About Project</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="content-text">
            This project was created by Stevanus Felixiano. It aims to provide a simple and effective tool for generating color palettes from images. By uploading an image, users can extract the most dominant colors, which can be useful for design, art, and various creative projects.
        </div>
        <div class="sub-header">Project Purpose</div>
        <div class="content-text">
            This page allows users to upload an image, and the application will generate a color palette based on the most dominant colors in the image. It provides a visual representation of these colors along with their corresponding hex codes.
        </div>
    """, unsafe_allow_html=True)

elif app_mode == "Color Palette Generator":
    st.markdown('<div class="main-header">DOMINANT COLOR PALETTE GENERATOR</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = load_image(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Analyzing image..."):
            colors = get_palette(image, n_colors=9)
            st.markdown('<div class="color-container">', unsafe_allow_html=True)
            for color in colors:
                st.markdown(f'''
                    <div class="color-item">
                        <div class="color-box" style="background-color: rgb{tuple(color)};"></div>
                        <div>RGB: {tuple(color)}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            plot = plot_palette(colors)
            st.pyplot(plot)
