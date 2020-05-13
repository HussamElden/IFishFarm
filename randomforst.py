import pickle
import preproccesing
import cv2
import joblib


class randomforst:

    def __init__(self):

        self.loaded_model = pickle.load(open("RandomForest400", 'rb'))
        self.scaler = joblib.load('scaler.pkl')

    def classify(self,mylist,mask,fps):
        image = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        arrofavg = preproccesing.featuresCalc(mylist,fps)
        cnt = image.size - cv2.countNonZero(image)
        arrofavg.append(cnt)
        arrofavg = self.scaler.transform([arrofavg])
        prediction = self.loaded_model.predict(arrofavg)
        return prediction