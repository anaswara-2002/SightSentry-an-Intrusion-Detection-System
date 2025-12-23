import os
from flask import Flask, render_template, Response, request, redirect, url_for, g
from werkzeug.utils import secure_filename
import cv2
from simple_facerec import SimpleFacerec
import pygame
import sqlite3
from datetime import datetime

app = Flask(__name__)

ADMIN_USERNAME = 'Anaswara'
ADMIN_PASSWORD = '12345'
DB_NAME = 'database.db'
IMAGE_DIR = r'C:\Anaswara\source\images'

# Initialize pygame mixer
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load("static/alert.mp3")

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)



# Function to get the SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def gen_frames():
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error reading frame. Exiting...")
            break

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            # insertion logic
            current_datetime = datetime.now()
            string= str(name)+'  is  detected at  '+ str(current_datetime)
            with app.app_context():
                db = get_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO logs (logs) VALUES (?)", (string,))
                db.commit()
                cursor.close()

            if name == 'Unknown':
                 pygame.mixer.music.play()
                
            

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(IMAGE_DIR, filename)
            print("block5", image_path)
            try:
                image.save(image_path)
                print("Image saved successfully")
            except Exception as e:
                print("Error saving image:", e)
            # Add code to update the face recognition model with the new image
            # For example: sfr.add_encoding(image_path, filename)
            return redirect(url_for('admin'))

    cursor.execute('SELECT name, image_path FROM users')
    user_info = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', user_info=user_info)

if __name__ == "__main__":
    # Create logs table if not exists
    app.run(debug=True)