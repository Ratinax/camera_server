from flask import Flask, render_template, Response
import cv2
import threading
import ssl

app = Flask(__name__)

# Utilisez le chemin vers vos certificats SSL/TLS
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert.pem', 'key.pem')

cap = cv2.VideoCapture(0)
print(cap.isOpened())
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', content_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Utilisez un port et un hôte appropriés
    app.run(host='0.0.0.0', port=5000, ssl_context=context,threaded=True)