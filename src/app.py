from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend requests

# Load the YOLO model for license plate detection
model = YOLO('C:\\Users\\chari\\license_plate_detector.pt')
 
# Directory to save the cropped license plate images
output_dir = "C:\\Users\\chari\\Documents\\myapp\\lpr-pr\\public"

if not os.path.exists(output_dir): 
    
    os.makedirs(output_dir)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/detect-license-plates', methods=['POST'])
def detect_license_plates():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    image_path = os.path.join(output_dir, 'temp_image.jpg')
    image_file.save(image_path)
    print(f"Saved uploaded image to {image_path}")

    # Perform object detection on the image
    results = model(image_path)
    image = cv2.imread(image_path)
    print("Image loaded for detection")

    license_plate_detections = []
    for result in results:
        for det in result.boxes:
            det_cls = int(det.cls.item())
            if det_cls == 0:
                det_xyxy = [int(coord.item()) for coord in det.xyxy[0]]
                license_plate_detections.append(det_xyxy)

    output_files = []
    for i, license_plate in enumerate(license_plate_detections):
        x1, y1, x2, y2 = license_plate
        cropped_plate = image[y1:y2, x1:x2]
        output_path = os.path.join(output_dir, f"license_plate_{i+1}.jpg")
        cv2.imwrite(output_path, cropped_plate)
        print(f"Saved cropped license plate to {output_path}")
        output_files.append(f"/output/license_plate_{i+1}.jpg")  # Adjusted path

    return jsonify({'files': output_files})

@app.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
