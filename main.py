import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from ultralytics import YOLO
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import tkintermapview
from geopy.geocoders import Nominatim
import geocoder

class RedTheme(ttk.Style):
    def __init__(self):
        super().__init__()
       
        self.primary_bg = '#1a0505'      
        self.secondary_bg = '#2b0808'    
        self.accent_red = '#cf1515'      
        self.text_color = '#ff9999'      
        
        self.configure('Main.TFrame', background=self.primary_bg)
        self.configure('Main.TLabel', 
                      background=self.primary_bg, 
                      foreground=self.text_color)
        self.configure('Main.TButton', 
                      background=self.accent_red,
                      foreground=self.text_color,
                      padding=10,
                      font=('Helvetica', 10, 'bold'))
        self.configure('Alert.TButton',
                      background='#ff0000',
                      foreground=self.text_color,
                      padding=10,
                      font=('Helvetica', 10, 'bold'))

class ViolenceDetectionUI:
    def __init__(self, window):
        self.window = window
        self.window.title("HER SHIELD")
        self.window.configure(bg='#1a0505')
        
        self.style = RedTheme()
        
        self.violence_model = load_model(r'D:\MODELS\model_v_nv\model.h5')
        self.gender_model = YOLO(r"best.pt")
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.input_size = (128, 128)
        self.violence_threshold = 50
        self.is_recording = False
        self.alert_active = False
        
        # Initialize location services
        self.geolocator = Nominatim(user_agent="hershield")
        
        self.setup_ui()
        
        self.process_thread = threading.Thread(target=self.process_video, daemon=True)
        self.process_thread.start()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))

        header_text = ttk.Label(header_frame, 
                              text="🛡️ HER SHIELD",
                              style='Main.TLabel',
                              font=('Helvetica', 24, 'bold'))
        header_text.pack()

        content_frame = ttk.Frame(main_frame, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left side - Video
        video_frame = ttk.Frame(content_frame, style='Main.TFrame')
        video_frame.pack(side=tk.LEFT, padx=5)
        self.video_label = ttk.Label(video_frame, style='Main.TLabel')
        self.video_label.pack()

        # Right side - Controls and Map
        right_frame = ttk.Frame(content_frame, style='Main.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Controls
        control_frame = ttk.Frame(right_frame, style='Main.TFrame')
        control_frame.pack(fill=tk.X, pady=5)

        status_frame = ttk.Frame(control_frame, style='Main.TFrame')
        status_frame.pack(fill=tk.X, pady=5)
        self.status_indicator = ttk.Label(status_frame, 
                                        text="⬤",
                                        style='Main.TLabel',
                                        foreground="#00ff00")
        self.status_indicator.pack(side=tk.LEFT)
        ttk.Label(status_frame, 
                 text="System Active",
                 style='Main.TLabel').pack(side=tk.LEFT, padx=5)

        self.record_btn = ttk.Button(control_frame, 
                                   text="🎥 RECORD",
                                   style='Main.TButton',
                                   command=self.toggle_recording)
        self.record_btn.pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame, 
                  text="👮 CONTACT POLICE",
                  style='Main.TButton',
                  command=lambda: self.trigger_alert("Police contacted")).pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame,
                  text="🏥 CONTACT HOSPITAL",
                  style='Main.TButton',
                  command=lambda: self.trigger_alert("Hospital contacted")).pack(fill=tk.X, pady=2)
        
        ttk.Button(control_frame,
                  text="⚠ MANUAL ALERT",
                  style='Alert.TButton',
                  command=lambda: self.trigger_alert("Manual alert activated")).pack(fill=tk.X, pady=2)

        # Location info
        self.location_label = ttk.Label(control_frame,
                                      text="Current Location: Fetching...",
                                      style='Main.TLabel',
                                      font=('Helvetica', 10))
        self.location_label.pack(fill=tk.X, pady=5)

        # Map widget
        map_frame = ttk.Frame(right_frame, style='Main.TFrame')
        map_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.map_widget = tkintermapview.TkinterMapView(map_frame, width=400, height=200)
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        
        # Initialize map to a default location (will be updated when actual location is obtained)
        self.map_widget.set_zoom(15)

        # Alerts section
        ttk.Label(right_frame,
                 text="Recent Alerts",
                 style='Main.TLabel',
                 font=('Helvetica', 12, 'bold')).pack(pady=(20,5))
        
        self.alerts_text = tk.Text(right_frame,
                                 height=10,
                                 width=30,
                                 bg='#2b0808',
                                 fg='#ff9999',
                                 font=('Helvetica', 10))
        self.alerts_text.pack(fill=tk.BOTH, expand=True)

        # Initial location update
        self.update_location()

    def get_current_location(self):
        """Get current location using IP-based geolocation"""
        g = geocoder.ip('me')
        if g.ok:
            return g.latlng, g.address
        return None, "Location unavailable"

    def update_location(self):
        """Update the current location and map"""
        coords, address = self.get_current_location()
        if coords:
            lat, lng = coords
            self.location_label.configure(text=f"Location: {address}")
            self.map_widget.set_position(lat, lng)
            self.map_widget.set_marker(lat, lng, text="Current Location")
        else:
            self.location_label.configure(text="Location: Unable to fetch location")

    def process_frame(self, frame):
        start_time = time.time()
        
        # Violence detection
        img = cv2.resize(frame, self.input_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        prediction = self.violence_model.predict(img, verbose=0)
        class_label = np.argmax(prediction, axis=1)
        confidence = np.max(prediction) * 100
        
        # Gender detection
        results = self.gender_model(frame, verbose=False)
        
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = box.cls[0]
                gender = "female" if cls == 0 else "male"
                color = (0, 0, 255) if gender == "female" else (255, 0, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{gender} {conf:.2f}", (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        if class_label[0] == 0 and confidence > self.violence_threshold:
            cv2.putText(frame, 'VIOLENCE DETECTED', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            if not self.alert_active:
                self.trigger_alert("Violence detected!")
                self.status_indicator.configure(foreground="red")
                self.window.after(1000, lambda: self.status_indicator.configure(foreground="#00ff00"))
                # Update location when violence is detected
                self.update_location()
        
        process_time = (time.time() - start_time) * 1000
        cv2.putText(frame, f"Latency: {process_time:.1f}ms", (10, frame.shape[0]-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        return frame

    def process_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            frame = self.process_frame(frame)
            
            if self.is_recording:
                cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)
            
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.record_btn.configure(text="⏹ STOP RECORDING")
            self.trigger_alert("Recording started")
        else:
            self.record_btn.configure(text="🎥 RECORD")
            self.trigger_alert("Recording stopped")

    def trigger_alert(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        coords, address = self.get_current_location()
        if coords:
            lat, lng = coords
            location_info = f"\nLocation: {address}\nCoordinates: {lat:.6f}, {lng:.6f}"
        else:
            location_info = "\nLocation: Unable to fetch location"
            
        self.alerts_text.insert('1.0', f"[{timestamp}] {message}{location_info}\n{'-'*40}\n")
        self.alert_active = True
        self.window.after(5000, self.reset_alert)

    def reset_alert(self):
        self.alert_active = False

    def cleanup(self):
        self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = ViolenceDetectionUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cleanup(), root.destroy()))
    root.mainloop()