import cv2
import numpy as np
import math
from PIL import Image
from sklearn.decomposition import PCA


class HandJointAngles():

    import numpy as np
    from sklearn.decomposition import PCA

    def __init__(self):

        self.HAND_KEYPOINTS = ["WRIST",
          "THUMB_CMC",
          "THUMB_MCP" ,
          "THUMB_IP",
          "THUMB_TIP",
          "INDEX_FINGER_MCP",
          "INDEX_FINGER_PIP",
          "INDEX_FINGER_DIP",
          "INDEX_FINGER_TIP",
          "MIDDLE_FINGER_MCP",
          "MIDDLE_FINGER_PIP",
          "MIDDLE_FINGER_DIP",
          "MIDDLE_FINGER_TIP",
          "RING_FINGER_MCP",
          "RING_FINGER_PIP",
          "RING_FINGER_DIP",
          "RING_FINGER_TIP",
          "PINKY_MCP",
          "PINKY_PIP",
          "PINKY_DIP",
          "PINKY_TIP"]


        self.HAND_VECTORS = {"TWC":["WRIST", "THUMB_CMC"],
                        "TCM":["THUMB_CMC", "THUMB_MCP"],
                        "TMI":["THUMB_MCP", "THUMB_IP"],
                        "TIT":["THUMB_IP", "THUMB_TIP"],
                        "IWM":["WRIST", "INDEX_FINGER_MCP"],
                        "IMP":["INDEX_FINGER_MCP", "INDEX_FINGER_PIP"],
                        "IPD":["INDEX_FINGER_PIP", "INDEX_FINGER_DIP"],
                        "IDT":["INDEX_FINGER_DIP", "INDEX_FINGER_TIP"],
                        "MWM":["WRIST", "MIDDLE_FINGER_MCP"],
                        "MMP":["MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"],
                        "MPD":["MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"],
                        "MDT":["MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"],
                        "RWM":["WRIST", "RING_FINGER_MCP"],
                        "RMP":["RING_FINGER_MCP", "RING_FINGER_PIP"],
                        "RPD":["RING_FINGER_PIP", "RING_FINGER_DIP"],
                        "RDT":["RING_FINGER_DIP", "RING_FINGER_TIP"],
                        "PWM":["WRIST", "PINKY_MCP"],
                        "PMP":["PINKY_MCP", "PINKY_PIP"],
                        "PPD":["PINKY_PIP", "PINKY_DIP"],
                        "PDT":["PINKY_DIP", "PINKY_TIP"]
        }

        self.HAND_JOINTS = {"WRIST_THUMB_INDEX":["TWC","IWM"],
                                "WRIST_THUMB":["TWC","TCM"],
                                "THUMB_1":["TCM","TMI"],
                                "THUMB_2":["TMI","TIT"],
                                "WRIST_INDEX":["IWM","IMP"],
                                "INDEX_1":["IMP","IPD"],
                                "INDEX_2":["IPD","IDT"],
                                "INDEX_MIDDLE":["IMP","MMP"],
                                "WRIST_MIDDLE":["MWM","MMP"],
                                "MIDDLE_1":["MMP","MPD"],
                                "MIDDLE_2":["MPD","MDT"]
        }


        def getHandVectors(self,data):
            for vector_name, points in self.HAND_VECTORS.items():
                print(vector_name)
                print(data[vector_name[1]]- data[vector_name[0]])


            
        self.HAND_JOINTS2 = {

                "ThumbAb": [("WRIST", "THUMB_CMC"), ("WRIST", "INDEX_FINGER_MCP")],
                "ThumbCM": [("WRIST", "THUMB_CMC"), ("THUMB_CMC", "THUMB_MCP")],
                "ThumbMP": [("THUMB_CMC", "THUMB_MCP"), ("THUMB_MCP", "THUMB_IP")],
                "ThumbIP": [("THUMB_MCP", "THUMB_IP"), ("THUMB_IP", "THUMB_TIP")],
                "IndexMP": [("WRIST", "INDEX_FINGER_MCP"), ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP")],
                "IndexPIP": [("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"), ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP")],
                "IndexDIP": [("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"), ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP")],
                "MiddleAb": [("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"), ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP")],
                "MiddleMP": [("WRIST", "MIDDLE_FINGER_MCP"), ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP")],
                "MiddlePIP": [("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"), ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP")],
                "MiddleDIP": [("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"), ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_TIP")]
        }



    def getAngle(self, vector1, vector2):
        inner_product = np.inner(vector1, vector2)
        norm_v1 = np.linalg.norm(vector1)
        norm_v2 = np.linalg.norm(vector2)

        if norm_v1 == 0.0 or norm_v2 == 0.0:
            return np.nan
        cos = inner_product / (norm_v1*norm_v2)
        # result in radians
        rad = np.arccos(np.clip(cos, -1.0, 1.0))
        # covert to degrees
        theta = np.rad2deg(rad)

        return theta



    def getJointAngle(self,vector1, vector2, hand_direction, hand_side="right"):

        if hand_side == "right":
            sign = 1
        else:
            sign = -1
    
        angle = self.getAngle(vector1, vector2)

        if np.isnan(angle):
            return angle

        cross_product = np.cross(vector1, vector2)
        direct_inner = np.inner(cross_product, hand_direction)

        if np.isnan(direct_inner):
            sign *= 1
        else:
            if direct_inner >= 0:
                sign *= 1
            else:
                sign *= -1
        res = sign * angle

        return res





def getClasses(path_deep_model):
    classesFile = path_deep_model + "/model.names"
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    return classes

class HumanDetector():

    def __init__(self):

        import mediapipe as mp

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_drawing_styles = mp.solutions.drawing_styles

        
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        # Initialize MediaPipe Hands.
        self.hands = self.mp_hands.Hands(static_image_mode=True,max_num_hands=2,min_detection_confidence=0.4)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.skeleton_detection = self.mp_pose.Pose(static_image_mode=True,model_complexity=2,enable_segmentation=True,min_detection_confidence=0.5)


        self.list_points = ["WRIST",
          "THUMB_CMC",
          "THUMB_MCP" ,
          "THUMB_IP",
          "THUMB_TIP",
          "INDEX_FINGER_MCP",
          "INDEX_FINGER_PIP",
          "INDEX_FINGER_DIP",
          "INDEX_FINGER_TIP",
          "MIDDLE_FINGER_MCP",
          "MIDDLE_FINGER_PIP",
          "MIDDLE_FINGER_DIP",
          "MIDDLE_FINGER_TIP",
          "RING_FINGER_MCP",
          "RING_FINGER_PIP",
          "RING_FINGER_DIP",
          "RING_FINGER_TIP",
          "PINKY_MCP",
          "PINKY_PIP",
          "PINKY_DIP",
          "PINKY_TIP"]

        self.dict_points = {"WRIST":{},"THUMB_CMC":{},"THUMB_MCP":{},
          "THUMB_IP":{},"THUMB_TIP":{},
          "INDEX_FINGER_MCP":{},"INDEX_FINGER_PIP":{},
          "INDEX_FINGER_DIP":{},"INDEX_FINGER_TIP":{},
          "MIDDLE_FINGER_MCP":{},"MIDDLE_FINGER_PIP":{},
          "MIDDLE_FINGER_DIP":{},"MIDDLE_FINGER_TIP":{},
          "RING_FINGER_MCP":{},"RING_FINGER_PIP":{},
          "RING_FINGER_DIP":{},"RING_FINGER_TIP":{},
          "PINKY_MCP":{},"PINKY_PIP":{},
          "PINKY_DIP":{},"PINKY_TIP":{}}

    def setHandsParameters(self,static_image_mode=True,max_num_hands=2,min_detection_confidence=0.4):
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,max_num_hands=max_num_hands,min_detection_confidence=min_detection_confidence)
    def setBodyParameters(self,min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.pose = self.mp_pose.Pose(min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)
    def setFaceParameters(self,model_selection=1, min_detection_confidence=0.5):
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=model_selection, min_detection_confidence=min_detection_confidence)


    def drawBody(self, image_src):
        new_image = image_src.copy()
        self.mp_drawing.draw_landmarks(
            new_image,
            self.hand_results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())


        return new_image
    
    def getBody(self, image_src):
        image_src.flags.writeable = False
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
        self.hand_results = self.skeleton_detection.process(image_src)
        y_resolution, x_resolution, c = image_src.shape

        # Draw the pose annotation on the image.
        image_src.flags.writeable = True
        image_src = cv2.cvtColor(image_src, cv2.COLOR_RGB2BGR)

        list_pose = ["NOSE",
            "LEFT_EYE_INNER",
            "LEFT_EYE",
            "LEFT_EYE_OUTER",
            "RIGHT_EYE_INNER",
            "RIGHT_EYE",
            "RIGHT_EYE_OUTER",
            "LEFT_EAR",
            "RIGHT_EAR",
            "MOUTH_LEFT",
            "MOUTH_RIGHT",
            "LEFT_SHOULDER",
            "RIGHT_SHOULDER",
            "LEFT_ELBOW",
            "RIGHT_ELBOW",
            "LEFT_WRIST",
            "RIGHT_WRIST",
            "LEFT_PINKY",
            "RIGHT_PINKY",
            "LEFT_INDEX",
            "RIGHT_INDEX",
            "LEFT_THUMB",
            "RIGHT_THUMB",
            "LEFT_HIP",
            "RIGHT_HIP",
            "LEFT_KNEE",
            "RIGHT_KNEE",
            "LEFT_ANKLE",
            "RIGHT_ANKLE",
            "LEFT_HEEL",
            "RIGHT_HEEL",
            "LEFT_FOOT_INDEX",
            "RIGHT_FOOT_INDEX"]

        init_value = {"x":0,"y":0, "p":0}
        pose_values = {};

        for element in list_pose:
            pose_values[element] = init_value
            #print(element)
            try:
                value = self.hands_results.pose_landmarks.landmark[self.mp_pose.PoseLandmark[element]]
                value.x, value.y = self._normalized_to_pixel_coordinates(value.x, value.y, x_resolution,y_resolution)
                pose_values[element] = {"x":value.x,"y":value.y, "p":1}
            except:
                pass
    
        return pose_values

    def drawFace(self, image_src):
        new_image = image_src.copy()
        for detection in self.face_results.detections:
            self.mp_drawing.draw_detection(new_image, detection)
        return new_image

    def getFace(self, image_src):

        image_src.flags.writeable = False
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
        self.face_results = self.face_detection.process(image_src)
        y_resolution, x_resolution, c = image_src.shape
        image_src.flags.writeable = True

        faces = {}
        if self.face_results.detections:
            for detection in self.face_results.detections:
                data = detection.location_data
                xmin = data.relative_bounding_box.xmin
                ymin = data.relative_bounding_box.ymin
                width = data.relative_bounding_box.width
                height= data.relative_bounding_box.height
                xmin, ymin = self._normalized_to_pixel_coordinates(xmin, ymin, x_resolution,y_resolution)
                width, height = self._normalized_to_pixel_coordinates(width, height, x_resolution,y_resolution)

                faces= {detection.label_id[0]:{"xmin":xmin, "ymin":ymin, "width":width, "height":height}}

                #print(detection.label_id[0])
                #print(data.relative_bounding_box.xmin)

            return faces



    def _getDistance(self,elementA,elementB):
        pixelX = elementA.x - elementB.x
        pixelY = elementA.y - elementB.y

        
        distance = (pixelX**2 + pixelY**2)**.5
        
        return distance
    

    def getHandFromPoseIndexes(self,wrist, elbow, shoulder, threshold = 0.03):

        
        ratioWristElbow = 0.33
        handRectangle_x = wrist.x + ratioWristElbow * (wrist.x - elbow.x)
        handRectangle_y = wrist.y + ratioWristElbow * (wrist.y - elbow.y)
        distanceWristElbow = self._getDistance(wrist, elbow)
        distanceElbowShoulder = self._getDistance(elbow, shoulder)
        handRectangle_width = 1.5 * max(distanceWristElbow, 0.9 * distanceElbowShoulder)



        handRectangle_height = handRectangle_width;
        #x-y refers to the center --> offset to topLeft point
        handRectangle_x = handRectangle_x - handRectangle_width / 2.0
        handRectangle_y = handRectangle_y - handRectangle_height / 2.0


        return int(handRectangle_x), int(handRectangle_y), int(handRectangle_width), int(handRectangle_height)


    def _normalized_to_pixel_coordinates(self, normalized_x, normalized_y, image_width,image_height):

      x_px = min(math.floor(normalized_x * image_width), image_width - 1)
      y_px = min(math.floor(normalized_y * image_height), image_height - 1)
      
      return x_px, y_px


    def getHands(self,image_src, draw_image = False):

        from google.protobuf.json_format import MessageToDict
        y_resolution, x_resolution, c = image_src.shape
        # Convert the BGR image to RGB, flip the image around y-axis for correct 
        # handedness output and process it with MediaPipe Hands.
        results = self.hands.process(cv2.flip(cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB), 1))
        # Print handedness (left v.s. right hand).
        # print(results.multi_handedness)

        
        self.data = {"Right": self.dict_points.copy(),"Left": self.dict_points.copy(), "l_data":False ,"r_data":False}

        k = 0
        hand_ = "left"

        if draw_image:
            image_ = cv2.flip(image_src.copy(), 1)

        if results.multi_hand_landmarks:

            hand_dict = []
            for idx, hand_handedness in enumerate(results.multi_handedness):
                handedness_dict = MessageToDict(hand_handedness)
                hand_dict.append(handedness_dict)

            
            for hand_landmarks in results.multi_hand_landmarks:
                j = 0
                for data_point in hand_landmarks.landmark:
                    print(data_point)

                    hand_ = hand_dict[k]["classification"][0]["label"]
                    hand_value = hand_.split("\r")
                    if hand_value[0] == "Left":
                        self.data["l_data"] = True
                    else:
                        self.data["r_data"] = True
                        
                        
                    self.data[hand_value[0]][self.list_points[j]] = {'x': data_point.x*x_resolution,'y': data_point.y*y_resolution }
                    j = j + 1
                if draw_image:
                    self.mp_drawing.draw_landmarks(image_, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                k = k + 1

        if draw_image:
            return  self.data, cv2.flip(image_, 1) 
        else:
            return  self.data, 0
 

class SSDObjectDetector():
    import cv2
    import numpy as np
    import time

    def __init__(self, classes, path_deep_model, fix_index = True, config = {"inpWidth":320,"inpHeight":320,"confThreshold":0.5, "nmsThreshold":0.5}):
        self.classes = classes
        self.config = config
        self.fix_index = fix_index
        self.confThreshold = config["confThreshold"]

        print("[INFO] Loading model...")

        self.net = cv2.dnn.readNetFromCaffe(path_deep_model + "/model.prototxt",  path_deep_model +  "/model.caffemodel")
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        print("[INFO] Model ready...")

    def getObjects(self,img):
        cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        image = Image.fromarray(cv2_im)
        # Runs the detection on a frame and return bounding boxes and predicted labels
        detections = self.predict_detection(img, self.net)
        self.detected = self.proccess_prediction(img, detections, self.confThreshold)
        return self.detected

    def drawObjects(self, img_src):

        new_image = img_src.copy()

        for value in self.detected: 
            startX = value["box"]["x"] 
            startY = value["box"]["y"] 
            endX = startX + value["box"]["w"] 
            endY = startY + value["box"]["h"]
            cv2.rectangle(new_image, (startX, startY), (endX, endY),(255, 0, 0), 2)
            labelPosition = endY - 5
            cv2.putText(new_image, value["label"], (startX, labelPosition),
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)

        # Put efficiency information. The function getPerfProfile returns the 
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(new_image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return new_image



    def predict_detection(self,frame, net):
        '''
        Predict the objects present on the frame
        '''
        # Conversion to blob
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
        #blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        # Detection and prediction with model
        self.net.setInput(blob)
        return self.net.forward()


    def proccess_prediction(self, frame, detections, threshold):
        '''
        Filters the predictions with a confidence threshold and draws these predictions
        '''

        detected = []
        (height, width) = frame.shape[:2]
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
        
            if confidence > threshold:
                # Index of class label and bounding box are extracted
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])

                # Retreives corners of the bounding box
                (startX, startY, endX, endY) = box.astype("int")
                label_ = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
                label = self.classes[idx]
                position = [(startX + endX)/2, (startY + endY)/2]
                w = endX - startX
                h = endY - startY

                detected.append({"label":label, "center":{"x":int(position[0]), "y":int(position[1])},  "box":{"x":int(startX), "y":int(startY), "w":int(w), "h":int(h)}, "confidence":float(confidence)})

        return detected


class YoloObjectDetector():

    import cv2
    import numpy as np
    import time
    from PIL import Image

    def __init__(self, classes, path_deep_model, use_gpu = False, fix_index = True, config = {"inpWidth":320,"inpHeight":320,"confThreshold":0.5, "nmsThreshold":0.5}):
        self.classes = classes
        self.config = config
        self.fix_index = fix_index
        self.confThreshold = config["confThreshold"]
        self.nmsThreshold =  config["nmsThreshold"]

        print("[INFO] Loading model...")

        modelConfiguration = path_deep_model + "/model.cfg";
        modelWeights = path_deep_model + "/model.weights";

        self.net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
            print("[INFO] Using GPU...")
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) # DNN_TARGET_OPENCL_FP16,DNN_TARGET_OPENCL,DNN_TARGET_CPU = 0
            print("[INFO] Using CPU...")

        print("[INFO] DL model ready...")


    def _getOutputsNames(self, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        if(self.fix_index == True):
            # Get the names of the output layers, i.e. the layers with unconnected outputs
            return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        else:
            # Get the names of the output layers, i.e. the layers with unconnected outputs
            return [layersNames[i-1] for i in net.getUnconnectedOutLayers()]

    # Remove the bounding boxes with  low confidence using non-maxima suppression
    def _postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        #list_labels = []
        #list_index = []
        detected = []


        for i in indices:
            index = i
            try:
                index = i[0]
            except:
                index = i
                pass
            box = boxes[index]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]

            if confidences[index] > 0.5:
                label = self.classes[classIds[index]]
                position = [left + width/2, top + height/2]
                #list_index.append(classIds[i])
                #list_labels.append(label)
                detected.append({"label":label,"center":{"x":int(position[0]), "y":int(position[1])}, "box":{"x":left, "y":top, "w":width, "h":height}, "confidence":confidences[index]})
        return detected

    def drawObjects(self, img_src):

        new_image = img_src.copy()

        for value in self.detected: 
            startX = value["box"]["x"] 
            startY = value["box"]["y"] 
            endX = startX + value["box"]["w"] 
            endY = startY + value["box"]["h"]
            cv2.rectangle(new_image, (startX, startY), (endX, endY),(255, 0, 0), 2)
            labelPosition = endY - 5
            cv2.putText(new_image, value["label"], (startX, labelPosition),
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)

        # Put efficiency information. The function getPerfProfile returns the 
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(new_image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return new_image
    
    def getObjects(self, img):

        blob = cv2.dnn.blobFromImage(img, 1/255, (self.config["inpWidth"], self.config["inpHeight"]), [0,0,0], 1, crop=False)
        
        # Sets the input to the network
        self.net.setInput(blob)
        
        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self._getOutputsNames(self.net))
     
        # Remove the bounding boxes with low confidence
        self.detected = self._postprocess(img, outs)

        return self.detected


