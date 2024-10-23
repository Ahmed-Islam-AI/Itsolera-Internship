import streamlit as st
import torch
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO

# Set page configuration
st.set_page_config(page_title="Retail Product Detection System", layout="wide", page_icon="🛒")

# Load YOLO model (use your trained model path here)
model = YOLO('models/best.pt')  # Replace with your trained YOLOv11 model path

# Product label mapping (replace with your actual product data)
product_data = {
    0: 'Bisconni Chocolate Chip Cookies 46.8gm',
    1: 'Coca Cola Can 250ml',
    2: 'Colgate Maximum Cavity Protection 75gm',
    3: 'Fanta 500ml', 
    4: 'Fresher Guava Nectar 500ml', 
    5: 'Fruita Vitals Red Grapes 200ml', 
    6: 'Islamabad Tea 238gm', 
    7: 'Kolson Slanty Jalapeno 18gm', 
    8: 'Kurkure Chutney Chaska 62gm', 
    9: 'LU Candi Biscuit 60gm', 
    10: 'LU Oreo Biscuit 19gm', 
    11: 'LU Prince Biscuit 55.2gm', 
    12: 'Lays Masala 34gm', 
    13: 'Lays Wavy Mexican Chili 34gm', 
    14: 'Lifebuoy Total Protect Soap 96gm',
    15: 'Lipton Yellow Label Tea 95gm', 
    16: 'Meezan Ultra Rich Tea 190gm', 
    17: 'Peek Freans Sooper Biscuit 13.2gm', 
    18: 'Safeguard Bar Soap Pure White 175gm', 
    19: 'Shezan Apple 250ml', 
    20: 'Sunsilk Shampoo Soft - Smooth 160ml', 
    21: 'Super Crisp BBQ 30gm', 
    22: 'Supreme Tea 95gm', 
    23: 'Tapal Danedar 95gm', 
    24: 'Vaseline Healthy White Lotion 100ml',
}

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
        }
        .stSidebar {
            background-color: #4b4b4b;
            color: #ffffff;
        }
        h1 {
            color: #1f77b4;
        }
        .css-1m5o2rp {
            font-size: 1.1em;
        }
        .detected-product {
            background-color: #1f77b4;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .css-ocqkz7 {
            color: black;
        }
        .live-camera-header {
            text-align: center;
            color: #1f77b4;
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        .live-camera-container {
            display: flex;
            justify-content: center;
            flex-direction: column;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🛒 Retail Product Detection System")
st.write("""
This AI-powered system helps retailers detect and classify products on shelves, providing real-time insights for efficient inventory management.
""")

# Sidebar logo and customization
st.sidebar.image("image.jpg", width=200)

# Sidebar for selecting input type
st.sidebar.header("Input Options")
input_option = st.sidebar.selectbox("Choose Input Type", ["Select Input Type", "📁 Image Upload", "📹 Live Camera Feed"])

if input_option == "📁 Image Upload":
    # Upload Product Image
    uploaded_file = st.sidebar.file_uploader("Upload a product image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Product Image', use_column_width=True)
        st.info("🔄 Processing image...")

        # Convert uploaded image to OpenCV format
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Progress bar
        with st.spinner("Analyzing the image..."):
            # Run YOLO model inference
            results = model(image)

        # Extract detections (boxes)
        detections = results[0].boxes
        if len(detections) > 0:
            st.write(f"Detected {len(detections)} products.")

            # Loop over each detection and display the information
            for det in detections.data:  # Access the detection data
                box = det[:4]  # Get box coordinates (x1, y1, x2, y2)
                confidence = det[4].item()  # Get confidence score
                class_label = int(det[5].item())  # Get class label as an integer
                product_name = product_data.get(class_label, "Unknown Product")  # Map label to product name

                # Display the detected information
                st.write(f"Product: {product_name}, Confidence: {confidence:.2f}")

                # Optional: Draw the bounding box on the image
                # Draw box on the image
                x1, y1, x2, y2 = map(int, box.tolist())  # Convert to int
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle

        else:
            st.write("No products detected.")

        # Draw boxes on the image (optional)
        result_image = results[0].plot()  # Plot with detections
        st.image(result_image, caption="Detected Products", use_column_width=True)

elif input_option == "📹 Live Camera Feed":
    st.write("🔴 Accessing live camera feed...")

    # Initialize camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera, change if necessary

    # Check if camera opened successfully
    if not cap.isOpened():
        st.error("❌ Error: Could not access camera.")
    else:
        stframe = st.empty()  # Streamlit empty frame to display live video

        # Start live detection with control button
        st.sidebar.markdown("---")
        st.sidebar.subheader("Live Detection Controls")
        start_detection = st.sidebar.button("Start Live Detection")
        stop_detection = st.sidebar.button("Stop Camera")

        # Live camera container
        st.markdown('<div class="live-camera-header">Live Product Detection</div>', unsafe_allow_html=True)
        live_camera_container = st.container()
        detection_count = live_camera_container.empty()

        last_detected_product = None  # To track the last detected product

        if start_detection:
            detection_counter = 0
            
            while True:
                # Read frame from the camera
                ret, frame = cap.read()

                if not ret:
                    st.error("❌ Error: Failed to capture frame.")
                    break

                # Run YOLO model inference on the frame
                results = model(frame)

                # Get the detections from YOLO
                detections = results[0].boxes

                if len(detections.data) > 0:
                    # Find the detection with the highest confidence
                    highest_confidence = 0
                    product_name = None
                    for det in detections.data:
                        confidence = det[4].item()  # Confidence score
                        class_label = int(det[5].item())  # Get class label as an integer
                        detected_product = product_data.get(class_label, "Unknown Product")  # Map label to product

                        # Check for highest confidence detection
                        if confidence > highest_confidence:
                            highest_confidence = confidence
                            product_name = detected_product

                    # Display only if the product is different or confidence is higher than previous
                    if product_name != last_detected_product or confidence > highest_confidence:
                        st.write(f"Product: {product_name} | Confidence: {highest_confidence:.2f}")
                        last_detected_product = product_name  # Update last detected product

                # Draw boxes on the frame and display it
                result_frame = results[0].plot()
                stframe.image(result_frame, channels="BGR", use_column_width=True)

                # Break the loop if the user stops the app
                if stop_detection:
                    break

            cap.release()  # Release the camera

# Display insights (only relevant for image upload)
if input_option == "Select Input Type":
    st.header("📊 Product Insights")
    st.write("🔍 Product availability status and stock levels:")
    stock_levels = pd.DataFrame({
        'Product': [
                    'Bisconni Chocolate Chip Cookies 46.8gm', 'Coca Cola Can 250ml', 
                    'Colgate Maximum Cavity Protection 75gm', 'Fanta 500ml', 'Fresher Guava Nectar 500ml', 
                    'Fruita Vitals Red Grapes 200ml', 'Islamabad Tea 238gm', 'Kolson Slanty Jalapeno 18gm', 
                    'Kurkure Chutney Chaska 62gm', 'LU Candi Biscuit 60gm', 'LU Oreo Biscuit 19gm', 
                    'LU Prince Biscuit 55.2gm', 'Lays Masala 34gm', 'Lays Wavy Mexican Chili 34gm', 
                    'Lifebuoy Total Protect Soap 96gm', 'Lipton Yellow Label Tea 95gm', 
                    'Meezan Ultra Rich Tea 190gm', 'Peek Freans Sooper Biscuit 13.2gm', 
                    'Safeguard Bar Soap Pure White 175gm', 'Shezan Apple 250ml', 
                    'Sunsilk Shampoo Soft - Smooth 160ml', 'Super Crisp BBQ 30gm', 
                    'Supreme Tea 95gm', 'Tapal Danedar 95gm', 'Vaseline Healthy White Lotion 100ml'
                ],
        'Stock Level': [
                        23, 5, 12, 23, 4, 8, 6, 7, 4, 3, 23, 12, 11, 
                        33, 25, 13, 13, 42, 19, 14, 15, 17, 43, 22, 34
                        ],
        'Restock Needed': [
                            False, True, False, False, True, False, False, 
                            True, False, False, True, False, False, True, 
                            False, False, True, False, False, True, False, 
                            False, True, False, False
                        ]
    })
    st.table(stock_levels)

    # Visualizing Stock Levels
    st.header("📈 Stock Visualization")
    st.bar_chart(stock_levels.set_index('Product')['Stock Level'])

    # Restocking suggestions
    st.write("📦 Restocking suggestions based on detection data:")
    if stock_levels['Restock Needed'].any():
        restock_products = stock_levels[stock_levels['Restock Needed']]['Product'].tolist()
        st.warning(f"⚠️ Products to Restock: {', '.join(restock_products)}")
    else:
        st.success("✅ No products need restocking at this time.")

# Footer
st.markdown("""
    <style>
        .footer {
            background-color: #1f77b4;
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            margin-top: 20px;
        }
        .footer a {
            color: #f5f5f5;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        <p>&copy; 2024 Created By AI Team Epsilon |
        Product Detection System Using YOLOv11</p>
        
    </div>
    """, unsafe_allow_html=True)