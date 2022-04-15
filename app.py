from asyncio.windows_events import NULL
from urllib import response
from flask import Flask, jsonify, redirect, render_template, request, Response, session, url_for
from flask_session import Session
from flask_cors import CORS
import requests
import cv2
from PIL import Image
import os

app = Flask(__name__)
cors = CORS(app)
Session(app)

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()

    # def get_frame(self):
    #     success, image = self.video.read()
    #     # We are using Motion JPEG, but OpenCV defaults to capture raw images,
    #     # so we must encode it into JPEG in order to correctly display the
    #     # video stream.
    #     ret, jpeg = cv2.imencode('.jpg', image)
        
    
    #     if cv2.waitKey(0)%256 == 32:
    #         cv2.imwrite("image_saved_code.jpg",jpeg)
    #     return jpeg.tobytes()
    
        
    
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        
session= {}

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    
    
    file = request.files['image']
    file.save('img-saved.jpg')
    image = Image.open('img-saved.jpg')
    new_image = image.resize((544, 544))
    new_image.save('image_resized.jpg')
        
    headers = {'Content-Type': 'image/jpeg','Access-Control-Allow-Origin':'*' }
    data = open('image_resized.jpg','rb').read()
    url = 'https://api-2445582032290.production.gw.apicast.io/v1/foodrecognition?user_key=b2e94e2bdaa97d4b4b3ba63dc433c8d5'
    response = requests.post(url, headers=headers, data=data)
    data =  response.json()
    session["data"] = data
    return redirect(url_for('data'))

@app.route('/data',methods=['GET'])
def data():
    data_got = session.get('data',None)
    return data_got
    
        
    


# @app.route('/video',methods=['GET','POST'])
# def video():
        
#     return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)