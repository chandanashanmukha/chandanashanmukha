import os
from flask import Blueprint, render_template, request, jsonify, current_app
import logging
import cv2
import numpy as np
from backend.utils.emoji_replacer import replace_with_emoji
from backend.utils.contour_detector import find_contour_detector
import base64

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

main_bp = Blueprint('main', __name__)

camera_status = "OFF"

@main_bp.route('/')
def index():
    logger.debug("Rendering index.html")
    template_dir = os.path.abspath(current_app.template_folder)
    logger.debug("Template directory: %s", template_dir)
    logger.debug("Contents of template directory: %s", os.listdir(template_dir))
    return render_template('index.html')

@main_bp.route('/set_camera_status', methods=['POST'])
def set_camera_status():
    global camera_status
    camera_status = request.json['status']
    logger.debug(f"Camera status set to: {camera_status}")
    return jsonify({'status': camera_status})

@main_bp.route('/process_frame', methods=['POST'])
def process_frame():
    if camera_status != "ON":
        logger.debug("Camera status is OFF, skipping frame processing")
        return jsonify({'frame': None})

    logger.debug("Processing frame")
    data = request.json['frame']
    img_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    contours = find_contour_detector(frame)
    if contours:
        frame = replace_with_emoji(frame, contours)

    _, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer).decode('utf-8')
    logger.debug("Frame processed and encoded")
    return jsonify({'frame': 'data:image/jpeg;base64,' + encoded_frame})
