from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import ssl
import string
from random import randint

app = Flask(__name__)

# Utilisez le chemin vers vos certificats SSL/TLS
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert.pem', 'key.pem')

# Mot de passe à vérifier (changez-le selon vos besoins)
correct_password = "bonjour"
cap = cv2.VideoCapture(0)
client = {}

def	getRandomString() -> str:
	chars = string.ascii_lowercase + string.digits
	str = ""
	for _ in range(32):
		str += chars[randint(0, 35)]
	return str

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
    print(request.cookies["sessionCookie"])
    if request.url in client and client[request.url] == request.cookies["sessionCookie"]:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', content_type='multipart/x-mixed-replace; boundary=frame')
    return None

@app.route('/check_password', methods=['POST'])
def check_password():
    # client_url = request.url
    data = request.get_json()
    password = data.get('password', '')
    valid = password == correct_password
    if valid:
        session = getRandomString()
        client[request.url] = session
        response = jsonify(valid=valid)
        response.set_cookie('sessionCookie', session, httponly=True)
        return response
    else:
        return jsonify(valid=valid)

if __name__ == "__main__":
    # Utilisez un port et un hôte appropriés
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True)
