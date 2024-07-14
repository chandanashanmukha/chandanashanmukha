import os
import sys
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
import logging

# Import the contour detector and emoji replacer
from .utils.contour_detector import find_contour_detector
from .utils.emoji_replacer import replace_with_emoji

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Determine the correct project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Set the template and static folder paths
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

logger.debug("Flask app initialized with template folder: %s", app.template_folder)
logger.debug("Flask app initialized with static folder: %s", app.static_folder)

# Check directory permissions and list contents
try:
    if os.access(app.template_folder, os.R_OK):
        contents = os.listdir(app.template_folder)
        logger.debug("Contents of template directory: %s", contents)
    else:
        raise PermissionError("Read permission denied")
except PermissionError as e:
    logger.error("Permission denied when accessing %s: %s", app.template_folder, e)
    sys.exit(1)  # Exit the application if permissions are incorrect
except Exception as e:
    logger.error("Unexpected error when accessing %s: %s", app.template_folder, e)
    sys.exit(1)  # Exit the application if an unexpected error occurs

# Initialize global variables
camera_status = "OFF"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_camera_status', methods=['POST'])
def set_camera_status():
    global camera_status
    camera_status = request.json['status']
    logger.debug(f"Camera status set to: {camera_status}")
    return jsonify({'status': camera_status})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global camera_status
    if camera_status == "ON":
        frame_data_url = request.json['frame']
        # Convert base64 data to image
        img_data = base64.b64decode(frame_data_url.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process frame to detect contours and overlay emojis
        contour_detectors = find_contour_detector(frame)
        if contour_detectors:
            frame_with_emojis = replace_with_emoji(frame, contour_detectors)
        else:
            frame_with_emojis = frame

        # Convert frame back to base64 to send to frontend
        retval, buffer = cv2.imencode('.jpg', frame_with_emojis)
        img_data = base64.b64encode(buffer).decode('utf-8')
        return jsonify({'frame': 'data:image/jpeg;base64,' + img_data})
    else:
        return jsonify({'frame': None})

if __name__ == '__main__':
    app.run(debug=True)
