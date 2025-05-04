# yolo_api.py
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File 
app = FastAPI()

from PIL import Image
import io

def get_image_tags_yolov8_file(uploaded_file: UploadFile) -> list:
    """
    Accepts an uploaded image (FastAPI UploadFile), runs YOLOv8, and returns detected tags.

    :param uploaded_file: Image file uploaded via FastAPI
    :return: List of detected object tags
    """
    try:
        # Load YOLOv8 model
        model = YOLO("yolov8n.pt")  # You can change this to yolov8s.pt, yolov8m.pt, etc.

        # Read the uploaded image as bytes and convert to PIL image
        image_bytes = uploaded_file.file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        width, height = image.size  # Dimensions
        size_bytes = len(image_bytes)  # File size in bytes

        dimension = str(width) + " x " + str(height)
        size = round(len(image_bytes)/1024, 2)
        # Run detection
        results = model(image)

        # Extract tags from result
        tags = set()
        for result in results:
            for cls_id in result.boxes.cls:
                class_name = model.names[int(cls_id)]
                tags.add(class_name)

        return list(tags), dimension, str(size)

    except Exception as e:
        print(f"YOLOv8 Tag Extraction Error: {e}")
        return [], '', ''

