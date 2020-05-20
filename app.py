from flask import Flask, render_template, request, redirect, url_for, session, Response
import re
import mysql.connector
from numpy.linalg import norm
import cv2
import sys
import os
import math
import numpy as np
import json
from threading import Thread
import VideoEnhancement
import fishpredictor
import detector
import kmeancluster
import preproccesing
import randomforst

class fishs:
    def __init__(self):
        self.mylist = []
    def addfish(self,data):
        x=[data]
        self.mylist.append(x)
    def addframe(self,id,data):
        # print(len(self.mylist))
        if len(self.mylist)>(id-1):
            self.mylist[id-1].append(data)
        else:
            self.addfish(data)


app = Flask(__name__)
app.secret_key = "abc"

# # Enter your database connection details below

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "",
#     database = "samak"
# )
# mycursor = mydb.cursor()
waterIsToxic = "Clear"
isFinished = False
currentBehavior = "Normal"
cap = cv2.VideoCapture('chaos1.avi')

def yolo():
    cluster = kmeancluster.kmeans()
    classifier = randomforst.randomforst()
    samak = []
    framenum = 0
    sum = 0
    max = 0
    mylist = [[]]
    yolo = detector.detector()
    ret, frame = cap.read()
    fheight, fwidth, channels = frame.shape
    resize = False
    if (fheight > 352 or fwidth > 640):
        resize = True
        fwidth = 640
        fheight = 352
        frame = cv2.resize(frame, (640, 352))

    mask = np.zeros_like(frame)
    # Needed for saving video
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    dt_string = datetime.now().strftime("%H_%M_%S_%d_%m_%y")
    num_seconds = 10
    video = cv2.VideoWriter('videonormal/' +str(num_seconds*round(fps))+'_'+str(dt_string)+'.avi', fourcc, fps, (fwidth, fheight))
    # Read until video is completed
    counter = 0
    buffer = [[]]
    apperance = [[]]
    last_changed = []
    top = 0
    frms = 0

    # Needed to track objects
    n_frame = 8
    ref_n_frame_axies = []
    ref_n_frame_label = []
    ref_n_frame_axies_flatten = []
    ref_n_frame_label_flatten = []
    frm_num = 1
    coloredLine = np.random.randint(0, 255, (10000, 3))
    arr = []
    label_cnt = 1
    min_distance = 50
    while (cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            if frms % 2 == 0:
                img = VideoEnhancement.enhanceVideo(img, resize)
                v = 0
                cur_frame_axies = []
                cur_frame_label = []
                height, width, channels = img.shape
                boxes, confidences, centers, colors = yolo.detect(img)
                counter += 1
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.4)
                font = cv2.FONT_HERSHEY_PLAIN
                fishcounter = 1
                for i in range(len(boxes)):
                    if i in indexes:
                        lbl = float('nan')
                        x, y, w, h, = boxes[i]
                        center_x, center_y = centers[i]
                        color = colors[0]
                        if (len(ref_n_frame_label_flatten) > 0):
                            b = np.array([(center_x, center_y)])
                            a = np.array(ref_n_frame_axies_flatten)
                            distance = norm(a - b, axis=1)
                            min_value = distance.min()
                            if (min_value < min_distance):
                                idx = np.where(distance == min_value)[0][0]
                                lbl = ref_n_frame_label_flatten[idx]
                                points = (int(ref_n_frame_axies_flatten[idx][0]), int(ref_n_frame_axies_flatten[idx][1]))
                                mask = cv2.line(mask, (center_x, center_y), points, coloredLine[lbl].tolist(), 2)
                                cv2.circle(img, points, 5, coloredLine[lbl].tolist(), -1)

                        if (math.isnan(lbl)):
                            lbl = label_cnt
                            label_cnt += 1

                        arr.append([counter, lbl, center_x, center_y])
                        cur_frame_label.append(lbl)
                        cur_frame_axies.append((center_x, center_y))

                        samak.append([lbl, x, y, w, h])
                        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(img, '{}{}'.format("Fish", lbl), (x, y - 5), font, 1, (255, 255, 255), 2)

                if (len(ref_n_frame_axies) == n_frame):
                    del ref_n_frame_axies[0]
                    del ref_n_frame_label[0]

                ref_n_frame_label.append(cur_frame_label)
                ref_n_frame_axies.append(cur_frame_axies)
                ref_n_frame_axies_flatten = [a for ref_n_frame_axie in ref_n_frame_axies for a in ref_n_frame_axie]
                ref_n_frame_label_flatten = [b for ref_n_frame_lbl in ref_n_frame_label for b in ref_n_frame_lbl]
                z = sorted(samak, key=itemgetter(0))
                samak = []

                if (len(z) != 0):
                    fishpredictor.predictfish(z, apperance, buffer, last_changed, top, img, color, mylist, framenum)

                img = cv2.add(img, mask)
                # cv2.imshow("Image", img)
                mylist.append([])
                framenum += 1
                print(frms)
                print("----------")
                # cap.set(1,frms)
                video.write(img)
                if (frms % (round(fps) * num_seconds) == 0 and frms!=0):
                    result = cluster.classify(mask)

                    randomForestResult = (classifier.classify(z, mask,fps))
                    print(randomForestResult)

                    if (result == 1 or randomForestResult[0] == 1 or randomForestResult[0] == 2):
                        with open('exceltext/' + str(frms)+'_'+str(dt_string)+ '.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(mylist)
                            # writer.writerows(preproccesing.featuresCalc(mylist))
                        cv2.imwrite("trajecstest" + str(frms)+'_'+str(dt_string) + ".png", mask)

                        video.release()

                        dt_string = datetime.now().strftime("%H_%M_%S_%d_%m_%y")

                        video = cv2.VideoWriter('videotest/' + str(frms+(num_seconds*round(fps)))+'_'+str(dt_string)+'.avi', fourcc, fps,
                                                (fwidth, fheight))
                    print("result " + str(result))
                    global currentBehavior
                    if (randomForestResult[0] == 1):
                        currentBehavior = "Hunger"
                    
                    elif(randomForestResult[0] == 0):
                        currentBehavior = "Normal"
                    
                    elif(randomForestResult[0] == 2):
                        currentBehavior = "Obstacle in pond"
                        
                    mask = np.zeros_like(frame)
                    ref_n_frame_axies = []
                    ref_n_frame_label = []
                    ref_n_frame_axies_flatten = []
                    ref_n_frame_label_flatten = []
                    buffer = [[]]
                    apperance = [[]]
                    last_changed = []
                    # frms = 0
                    counter = 0
                    mylist = [[]]
                    framenum = 0
                    fishcounter = 1
                    label_cnt = 1
                    top = 0

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

                # Break the loop
        else:
            break
        frms += 1

    cap.release()
    cv2.destroyAllWindows()
    video.release()

@app.route('/', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username,  password))
        account = mycursor.fetchone()
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return redirect(url_for('home'))

        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg = msg)

@app.route('/pond')
def pond():
    # return render_template('home.html', username=session['username'])
    return render_template('home.html')


@app.route('/alert')
def alert():
    return render_template('alert.html')

@app.route('/home')
def home():
    return render_template('template.html')

@app.route('/stats')
def stats():
    return render_template('graphs.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('id', None)

    return redirect(url_for('login'))

def get_frame():
    #cap=cv2.VideoCapture('vid.mp4') #read vid
    global cap
    Thread(target = yolo).start()
    while (cap.isOpened()):
        retval, im = cap.read()
        if im is not None and retval:  #retval when false means last frame
            imgencode=cv2.imencode('.jpg',im)[1]
            cv2.waitKey(int((1/30)*1000))
            stringData=imgencode.tostring()
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        else:
            break
            cap.release()
    global isFinished
    isFinished = True


@app.route('/calc')
def calc():
    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/getYoloData', methods=['POST', 'GET'])
def getYoloData():
    global waterIsToxic, currentBehavior
    if isFinished:
        data = {'waterStatus': "Stream is not running", 'currentBehavior': "Stream is not running"}
    else:
        data = {'waterStatus': waterIsToxic, 'currentBehavior': currentBehavior}
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
