from flask import Flask, Response, render_template, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from ultralytics import YOLO # you only look once 
import threading
from datetime import datetime

app = Flask(__name__)

# Global variables
camera = None
output_frame = None
lock = threading.Lock()
alerts = []

# Load models
violence_model = load_model(r'D:\MODELS\model_v_nv\model.h5')
gender_model = YOLO(r"best.pt")
input_size = (128, 128)
violence_threshold = 40

def generate_frames():
    global output_frame, camera, alerts
    
    if camera is None:
        camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        # Violence Detection
        img = cv2.resize(frame, input_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Make violence prediction
        prediction = violence_model.predict(img)
        confidence = np.max(prediction) * 100
        class_label = np.argmax(prediction, axis=1)
        label = 'Violent' if class_label[0] == 0 else 'Non-Violent'
        
        # Gender Detection
        gender_results = gender_model(frame)
        annotated_frame = gender_results[0].plot()
        
        # Add violence detection overlay
        if label == 'Violent' and confidence > violence_threshold:
            cv2.putText(annotated_frame, 'VIOLENCE DETECTED', (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            
            # Record alert with additional information
            alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get gender detection results
            detected_objects = gender_results[0].boxes.data.tolist()
            gender_counts = {'Male': 0, 'Female': 0}
            for detection in detected_objects:
                class_id = int(detection[5])
                gender = 'Male' if class_id == 0 else 'Female'
                gender_counts[gender] += 1
            
            # Create detailed alert
            alert_info = {
                "time": alert_time,
                "violence_confidence": f"{confidence:.2f}%",
                "males_detected": gender_counts['Male'],
                "females_detected": gender_counts['Female']
            }
            alerts.append(alert_info)
            alerts = alerts[-10:]  # Keep only last 10 alerts
        
        # Add violence confidence display
        # cv2.putText(annotated_frame, f"Violence Confidence: {confidence:.2f}%", 
                #    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                #    (0, 0, 255) if confidence > violence_threshold else (0, 255, 0), 2)
        
        # Encode the frame
        with lock:
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            output_frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')

@app.route('/')
def index():
    return render_template('nindex.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_alerts')
def get_alerts():
    return jsonify({'alerts': alerts})

@app.route('/get_status')
def get_status():
    if camera is None or not camera.isOpened():
        status = "Camera Offline"
    else:
        status = "Active Monitoring"
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)