import cv2
from sklearn.linear_model import LinearRegression
import numpy as np
def prediction(c):
    data=[]
    for i in range(len(c)-1):
        data.append([c[i],c[i+1]])


    X = np.array(data)[:, 0].reshape(-1, 1)
    y = np.array(data)[:, 1].reshape(-1, 1)
    to_predict_x = [c[len(c)-1]]
    to_predict_x = np.array(to_predict_x).reshape(-1, 1)

    regsr = LinearRegression()
    regsr.fit(X, y)

    predicted_y = regsr.predict(to_predict_x)

    return  int(predicted_y)

font = cv2.FONT_HERSHEY_PLAIN

def predictfish(fishs, apperance, buffer, last_changed, top, img, color, mylist, framenum):
    if (top < fishs[-1][0]):
        top = fishs[-1][0]
        # print(z[-1][0])
    fishcounter = 1
    for i in range(len(fishs)):
        templabel = fishs[i][0]
        if (fishcounter != templabel):  # predict fish
            while (fishcounter < templabel):

                if (apperance[fishcounter] > 1):
                    px = 0
                    py = 0
                    px = prediction(buffer[fishcounter][0])
                    py = prediction(buffer[fishcounter][1])
                    if (px < 10000 and py < 10000 and px > -10000 and py > -10000):
                        if (len(buffer[fishcounter]) <= 8):
                            buffer[fishcounter][0].append(px)
                            buffer[fishcounter][1].append(py)
                            last_changed[fishcounter - 1] += 1
                            apperance[fishcounter] += 1
                        else:
                            if (last_changed[fishcounter - 1] == 8):
                                last_changed[fishcounter - 1] = 1
                                buffer[fishcounter][0][1] = px
                                buffer[fishcounter][1][1] = py
                            else:
                                # print(last_changed[fishcounter - 1])
                                buffer[fishcounter][0][last_changed[fishcounter - 1] - 1] = px
                                buffer[fishcounter][1][last_changed[fishcounter - 1] - 1] = py
                                last_changed[fishcounter - 1] += 1

                        cv2.rectangle(img, (px, py), (px + fishs[i][3], py + fishs[i][4]), color, 2)
                        mylist[framenum].append(px)
                        mylist[framenum].append(py)
                        cv2.putText(img, '{}{}'.format("added ", fishcounter), (px, py - 5), font, 1, (255, 255, 255),
                                    2)

                    else:
                        mylist[framenum].append(0)
                        mylist[framenum].append(0)
                else:
                    mylist[framenum].append(0)
                    mylist[framenum].append(0)

                fishcounter += 1
        if (fishcounter == templabel):  ##detected fish
            fishcounter += 1

            mylist[framenum].append(fishs[i][1])
            mylist[framenum].append(fishs[i][2])
            if (len(buffer) <= templabel):
                buffer.append([[fishs[i][1]], [fishs[i][2]]])
                apperance.append(1)
                last_changed.append(1)
            else:
                if (len(buffer[templabel]) <= 8):
                    buffer[templabel][0].append(fishs[i][1])
                    buffer[templabel][1].append(fishs[i][2])
                    last_changed[templabel - 1] += 1
                    apperance[templabel] += 1
                else:
                    if (last_changed[templabel - 1] == 8):
                        last_changed[templabel - 1] = 1
                        buffer[templabel][0][1] = fishs[i][1]
                        buffer[templabel][1][1] = fishs[i][2]
                    else:
                        last_changed[templabel - 1] += 1
                        buffer[templabel][0][last_changed[templabel - 1] - 1] = fishs[i][1]
                        buffer[templabel][1][last_changed[templabel - 1] - 1] = fishs[i][2]
    for i in range((fishs[-1][0]), top):  ##predeict rest of fish
        if (apperance[fishcounter] > 1):
            px = 0
            py = 0
            px = prediction(buffer[fishcounter][0])
            py = prediction(buffer[fishcounter][1])
            if (px < 10000 and py < 10000 and px > -10000 and py > -10000):
                if (len(buffer[fishcounter]) <= 8):
                    buffer[fishcounter][0].append(px)
                    buffer[fishcounter][1].append(py)
                    last_changed[fishcounter - 1] += 1
                    apperance[fishcounter] += 1
                else:
                    if (last_changed[fishcounter - 1] == 8):
                        last_changed[fishcounter - 1] = 1
                        buffer[fishcounter][0][1] = px
                        buffer[fishcounter][1][1] = py
                    else:
                        # print(last_changed[fishcounter - 1])
                        buffer[fishcounter][0][last_changed[fishcounter - 1] - 1] = px
                        buffer[fishcounter][1][last_changed[fishcounter - 1] - 1] = py
                        last_changed[fishcounter - 1] += 1
                cv2.rectangle(img, (px, py), (px + fishs[0][3], py + fishs[0][4]), color, 2)
                mylist[framenum].append(px)
                mylist[framenum].append(py)
                cv2.putText(img, '{}{}'.format("added ", fishcounter), (px, py - 5), font, 1, (255, 255, 255), 2)
                # print("predicted a fish" + str(fishcounter))
            else:
                mylist[framenum].append(0)
                mylist[framenum].append(0)
        else:
            mylist[framenum].append(0)
            mylist[framenum].append(0)
        fishcounter += 1
