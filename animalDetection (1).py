from imutils.video import VideoStream
from flask import Response
from flask import Flask, request
from flask import render_template
from time import sleep
import numpy as np
import subprocess
import threading
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
from twilio.rest import Client

#After 1 year.
#After 1 year once again. 
BUZZER = 25
PIR = 23


GPIO.setmode(GPIO.BCM)

number = 0

capture = 0

detection = 0

detcount = 0

detected = 0

GPIO.setup(BUZZER,GPIO.OUT)

GPIO.setup(PIR,GPIO.IN)

ap = argparse.ArgumentParser()

ap.add_argument("-c", "--probability", type = float, default = 0.2, help = "minimum probability to filter weak detections")

args = vars(ap.parse_args())


outputFrame = None

motionoutput = ""

lock = threading.Lock()



app = Flask(__name__)




vs = VideoStream(src=0).start()#enabel the camera to start capturing



time.sleep(2.0)


@app.route("/",methods = ['GET', 'POST'])


def index():

        global capture

        global detection

        global detcount

        global motionoutput

        global number

        global detected

        if request.method == "POST":

                
                if request.form.get("buzzeroff") == "buzzeroff":

                        GPIO.output(BUZZER,GPIO.LOW)

                if request.form.get("buzzeron") == "buzzeron":

                        GPIO.output(BUZZER,GPIO.HIGH)

                               


        return render_template("index.html",name = motionoutput)


def detect_motion(frameCount):

      

        global vs, outputFrame, lock

        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",

        "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]



        COLORS = np.random.uniform(0, 255, size = (len(CLASSES), 3))



# load our serialized model from disk

        print("[INFO] loading model...")

        net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


        # loop over frames from the video stream

        

        global capture

        global detection

        global detcount

        global motionoutput

        global detected

        

        while True:

                if detected == 1:
                        print("Animal Found")

                        #Soumya
                        '''account_sid = "		",#Account_Sid

                        auth_token = " 		" #Authorized token

                        client = Client(account_sid, auth_token)



                        message = client.api.account.messages.create(

                        body='\nAlert \nAnimal Found - \n' + CLASSES[idx] ,

                        from_=' ', #twillio genertaed number

                        to=' '		#Receiver number'''

                        )
                                       

                                                #print(message.sid)

                        GPIO.output(BUZZER,GPIO.HIGH)

                        time.sleep(5)

                        GPIO.output(BUZZER,GPIO.LOW)

                # read the next frame from the video stream, resize it,

                frame = None

                # convert the frame to grayscale, and blur it

                

                if GPIO.input(PIR):

                        motionoutput = "Motion Detected"

                        capture = 1

                else:

                        motionoutput = "Motion Not Detected"

                if capture == 1:

                        

                        count = 0

                        frame = vs.read()



                        frame = imutils.resize(frame, width=1200)



        # grab the frame dimensions and convert it to a blob

        # Binary Large Object = BLOB

                        (h, w) = frame.shape[:2]

                        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)



                        # pass the blob through the network and get the detections

                        net.setInput(blob)

                        detections = net.forward()

                        #print(detections)
                        
                        #print(detections[0,0,0,2])

                        # loop over the detections

                        for i in np.arange(0, detections.shape[2]):

                                # extract the probability of the prediction

                                probability = detections[0, 0, i, 2]

        

                                # filter out weak detections by ensuring that probability is

                                # greater than the min probability

                                if probability > 0.2:

                                        # extract the index of the class label from the

                                        # 'detections', then compute the (x, y)-coordinates of

                                        # the bounding box for the object

                                        idx = int(detections[0, 0, i, 1])

                                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                                        (startX, startY, endX, endY) = box.astype("int")

                                        if (CLASSES[idx] == "horse" or CLASSES[idx] == "cow" or CLASSES[idx] == "sheep" or CLASSES[idx] == "dog" or CLASSES[idx] == "cat" or CLASSES[idx] == "bird"):

                                                label = "{}: {:.2f}%".format(CLASSES[idx], probability * 100)

                                                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)

                                                y = startY - 15 if startY - 15 > 15 else startY + 15

                                                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                                                detected = 1

                                                

                                        else:

                                                detected = 0

                        # grab the current timestamp and draw it on the frame



                        timestamp = datetime.datetime.now()



                        cv2.putText(frame, timestamp.strftime(



                                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),



                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 1)



                        #cv2.putText(frame, "Its Working Dude", (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 1)



                        
                        #print(detected)
                        

                        # acquire the lock, set the output frame, and release the

                        # lock



                        with lock:

                                if capture == 0:

                                        outputFrame = None

                                else:

                                        outputFrame = frame.copy()

                        #print(detected)

                        



def generate():



        # grab global references to the output frame and lock variables



        global outputFrame, lock

        global detected



        # loop over frames from the output stream



        while True:



                # wait until the lock is acquired



                with lock:



                        # check if the output frame is available, otherwise skip



                        # the iteration of the loop



                        if outputFrame is None:

                                continue


                        # encode the frame in JPEG format



                        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)



                        # ensure the frame was successfully encoded



                        if not flag:

                             continue







                # yield the output frame in the byte format



                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 



                        bytearray(encodedImage) + b'\r\n')

                





@app.route("/video_feed")



def video_feed():

        global detected

        # return the response generated along with the specific media

        

        # type (mime type)

        print(detected)

        return Response(generate(),



                mimetype = "multipart/x-mixed-replace; boundary=frame")

 
# check to see if this is the main thread of execution



if __name__ == '__main__':



        # construct the argument parser and parse command line arguments



        ap = argparse.ArgumentParser()



        #ap.add_argument("-i", "--ip", type=str, required=True,



                #help="ip address of the device")



        #ap.add_argument("-o", "--port", type=int, required=True,



        #       help="ephemeral port number of the server (1024 to 65535)")



        ap.add_argument("-f", "--frame-count", type=int, default=32,



                help="# of frames used to construct the background model")



        args = vars(ap.parse_args())


        # start a thread that will perform motion detection



        t = threading.Thread(target=detect_motion, args=(



                args["frame_count"],))



        t.daemon = True

        t.start()

        # start the flask app

        app.run(host='192.168.43.86', port=8009, debug=True,



                threaded=True, use_reloader=False)

if __name__=='__main__':



   app.run()



# release the video stream pointer



vs.stop()



GPIO.cleanup()
