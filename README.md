# IFishFarm
### Project Description:

Fish Farms have become important in the modern life as they have a huge contribution to the economy and ensures a reliable supply and wide distribution of fish globally. Fish farming is a tedious process that requires a lot of labor work. Lack of monitoring leads to fish loss so, monitoring fish farms automatically would lower the risks of fish loss. IFish Farm aims to automatically detect any anomalies in the fish ponds like fish abnormal behaviors which lower the risks of fish loss and increase fish production.

### The system can be divided into several blocks: 
* Image Enhancement phase using Multi-Scale Retinex algorithm (MSR).
* Object Detection phase using YOLO object detection algorithm.
* Fish Tracking between different video frames.
* Preparation and Calculation of gathered data.
* Abnormal Behavior classification using Random Forest algorithm.
* Different Reports for fish ponds.

### IFish Farm Full Demo 

[![Watch the video](https://cdn.discordapp.com/attachments/629107934827249665/725776110910046248/Untitled.png)](https://www.youtube.com/watch?v=b4kqffDzEYQ)

### Image Enhancement phase


Image enhancement is important for our system as it provides better visualization for the turbid underwater images. Also, it provides better visulaization of fish which give better fish detection. For this, we use the Multi-Scale Retinex (MSR) algorithm. Firstly, the image is passed to the Single-Scale Retinex which subtract the logarithm of the image from the logarithm of the same image but applied Gaussian filter to it. The image is then passed to the Multi-Scale Retinex to give better and efficient results. The difference of images before and after enhancmenent is shown in the image below. 

![](https://cdn.discordapp.com/attachments/629107934827249665/725780257088471120/beforeafter.jpg)

### YOLO Object Detection 
YOLO was used for detecting objects (fish) which has an acceptable real-time accuracy. The algorithm is one of the regression-based object detection algorithms where it estimates the classes and region of interests for the image in a single run for the algorithm. It works by applying a single neural network to the image as a whole. Then, the network divides the image into regions and predicts the probabilities for each region. YOLOv3 algorithm was used rather than YOLOv2 as it is the better version with more accurate results. For the model creation, 2000 images of gold fish were collected. Then, we labeled the images with bounding boxes using a labeling software, which generates a text file with the boxes' coordinates for each image in the dataset. We train the dataset with the YOLO tiny weights and then stopped the training after 9000 epochs because there was not a significant improvement in the average loss rate in the previous 2000 iterations as shown in the graph in figure 1. The yolov3 tiny weights was used for training instead of the yolov3 weights, because the tiny weights file is a light version of the yolov3 weights which is aimed at models with low number of classes (only 1 class in our case) while the original yolov3 weights version is aimed at models with a high number of classes (e.g. 80 classes.).

![](https://cdn.discordapp.com/attachments/629107934827249665/725782379318476872/ABOVEDETECTIION.jpg)

### Fish Tracking 
A unique label/id is given to each fish detected to be tracked across the video frames. Fish detection by YOLO does not track fish frame by frame so tracking fish between frames is essential as fish might be misclassified. Fish tracking works as follows, It takes the center points of each object in each frame and saves it to an array where it saves the objects' x and y positions for the previous 8 frames in the video. Each frame the distance is calculated using euclidean distance between each referenced coordinates and the current coordinates of each box. If the minimum distance found is less than 50 then its the same object (fish) otherwise, a new id is given to that fish. An illustration of fish tracking is shown in the figure below.

![](https://cdn.discordapp.com/attachments/629107934827249665/725785290828152972/fishtracking.png)

### Data Calculation and Preparation

The data preparation phase benefits from the detected box coordinates of each detected fish from YOLO. Data like speed, direction, skewness and fish spread in the pond were calculated.The data coordinates of each detected fish is collected where the rows represent each video frame and the columns represent the X and Y coordinates of each fish. For the fish speed feature calculation, distance between two points is calculated between each two rows (frames) respectively. After getting the distace the spped feature is now calcluated. For the fish direction calculation, a comparison is made between the fish coordinates with the previous frame and the current frame. If any changes occurred while comparing, the new direction is then saved as a feature. For the skewness calculation, a counter is made to count each time a fish direction has changed. While, if the direction of the previous frame is the same as the current one, the count does not increment as it meant that the fish was not moving. For the fish spread calculation, the highest and lowest coordinates of a frame is taken to calculate the distance which is considered as the range of spread the fish has in the current frame.

Fish trajectories are then extracted, they were created by using the referred points of each fish (object) previously listed in the tracking section. Each fish trajectory path is created by getting the referenced point and the existing point and drawing a path between them while drawing a circle in the middle of every box. A black background image (mask) was used to draw on it the fish trajectories. The figure below shows the fish trajectories, picture (A) shows the intial state. Image (B) shows the final state. while, image (C) shows the final image and the mask produced.

![](https://cdn.discordapp.com/attachments/629107934827249665/725788755624984747/visualizetrajs.jpg)

The last stage of data preparation is the normalization of features using Min-Max scaling to to be on a scale between 0 and 1.

### Abnormal Behavior Detection
The process of detecting abnormal behavior relies on the combined data that were prepared from the data preparation step. Firstly, the average of all the data collected are calculated. Secondly, another data is added where we get the number of black pixels from the mask image of the trajectories which helps in knowing whether the fish behavior is normal or abnormal. Finally, different algorithms were tested to detect abnormal behavior using these features. However, Random Forest was found to get better results so, in order to detect different behaviors Random Forest classification algorithm was used. A graph is shown below showing the different performance of different algorithms in detecting fish behaviors. Also, it shows the difference before normalizing the data and after normalizing it.

![](https://cdn.discordapp.com/attachments/629107934827249665/725790131549896831/chart.jpg)

### Reports

A reporting system was made in order to track fish farm production rate and help fish farmers to know what is happening in the fish farm throughout the time. D3.js library was used in order to visualize the reports. The data was retrieved from our database. The database carried important data about the system which made us visualize data like normal behaviors streaks where we calculate the amount of time the fish in a fish pond was acting normal. Also, another insight was made to calculate the rate of normal/abnormal behavior occurrence across the fish farm where the amount of time of each abnormal or normal behavior was counted to know if it reached a certain level. Finally, the common repeated behavior across a month was determined by knowing the amount of time a fish pond was normal or abnormal.

![](https://cdn.discordapp.com/attachments/629107934827249665/725791885993443370/main3.jpg)




