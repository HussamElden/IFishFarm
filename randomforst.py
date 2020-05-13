import pickle
import preproccesing
import cv2
class randomforst:

    def __init__(self):

        self.loaded_model = pickle.load(open("RandomForest400", 'rb'))

    def classify(self,mylist,mask):
        image = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        arrofavg = preproccesing.featuresCalc(mylist)
        cnt = image.size - cv2.countNonZero(image)
        arrofavg.append(cnt)
        prediction = self.loaded_model.predict(arrofavg)
        return prediction