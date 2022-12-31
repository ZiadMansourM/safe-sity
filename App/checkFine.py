from Models.fineDetailsModel import FineDetailsModel
import string
import cv2
import os, csv
import imutils
import matplotlib.pyplot as plt
import numpy as np
import skimage as sk
import skimage.measure
from skimage.morphology import binary_erosion
from typing import Final
import pickle

IMG_WIDTH, IMG_HEIGHT = 35, 45
digitLetter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class CheckFine():
    fineDetails: FineDetailsModel = None
    knnModel = None

    def __init__(self, jsonFile: string):
        self.fineDetails = FineDetailsModel(jsonFile)
        self.knnModel = pickle.load(open('knnpickle_file', 'rb'))
        pass

    def checkFine(self, licensePlate: string, government: string, city: string, street: string):
        images = self.fineDetails.getLicensePlates(government, city, street)
        if images == None:
            return None
        else:
            for image in images:
                text = self.processImage(image)
                if text == licensePlate.upper():
                    return image
            return None

    def processImage(self, path: string):
        img = cv2.imread(path)
        img = self.crop_image(img)
        img = self.segment_Character(img)
        text  = self.recognize_Character(img)
        return text
        
    # [1]: Crop Number Plate
    def crop_image(self, image: np.ndarray): #-> np.ndarray:
        # [0]: Local CONSTANTS
        CANNY_THRESH_LOW: Final[int] = 170
        CANNY_THRESH_HIGH: Final[int] = 200
        BILATERAL_FILTER_SIZE: Final[int] = 11
        BILATERAL_FILTER_SIGMA_COLOR: Final[int] = 17
        BILATERAL_FILTER_SIGMA_SPACE: Final[int] = 17
        MAX_NUM_CONTOURS: Final[int] = 30
        # [1]: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # [2]: Reduce noise and preserve edges
        gray = cv2.bilateralFilter(
            gray, 
            BILATERAL_FILTER_SIZE, 
            BILATERAL_FILTER_SIGMA_COLOR, 
            BILATERAL_FILTER_SIGMA_SPACE
        )
        # [3]: Edge Detection
        edges = cv2.Canny(gray, CANNY_THRESH_LOW, CANNY_THRESH_HIGH)
        # [4]: Find contours && sort by their area
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:MAX_NUM_CONTOURS]
        # [5]: Find contour with 4 corners
        def get_image(contour) -> np.ndarray:
            x, y, w, h = cv2.boundingRect(contour)
            return gray[y:y+h, x:x+w]
        temp=[
            get_image(c)
            for c in contours 
            if cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True).shape[0] == 4
        ]
        return temp[0] if temp else []

    # [2]: Skew Rotation Correction
    def rotate_image(self, image: np.ndarray) -> np.ndarray:
        # [0]: Local CONSTANTS
        CANNY_THRESH_LOW: Final[int] = 0
        CANNY_THRESH_HIGH: Final[int] = 100
        # [2]: Edge Detection
        edges = cv2.Canny(image, CANNY_THRESH_LOW, CANNY_THRESH_HIGH)
        # [3]: Hough Transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, 40)
        # [4]: Find most common angle
        angle = np.degrees(max(
            (line[0][1] for line in lines), 
            key=lambda x: list(lines[:,0,1]).count(x)
        ))
        # [5]: Rotate the image
        return sk.transform.rotate(
            image,
            angle+90 if angle<0 else angle-90
        )

    # [3]: Character Segmentation
    def segment_Character(self, image: np.ndarray) -> np.ndarray:
        Height,Width=image.shape
        # print(Height,Width)
        image_out = np.zeros(image.shape)
        # [1]: Threshold Image using OTSU for automatic thresholding
        Threshold = sk.filters.threshold_otsu(image)
        image_out[image <= Threshold] = 1
        # show_images([ image_out])

        # [2]: Detect Contours around each character
        contours = sk.measure.find_contours(image_out, 0.8)
        bounding_boxes = []
        for contour in contours:
            startY, endY = min(contour[:, 0]), max(contour[:, 0])
            startX, endX = min(contour[:, 1]), max(contour[:, 1])
            ratio = (endY-startY)/(endX-startX)
            if(1 < ratio < 3.5):
                tup = map(int, np.round((startX, endX, startY, endY)))
                # print(startY,endY,"Height",endY-startY,startX, endX,"Width",endX-startX)
                # bounding_boxes.append(tuple(tup))
                endY-startY > (0.25*Height) and endX - \
                    startX > (0.01*Width) and bounding_boxes.append(tuple(tup))
                # endY-startY > (0.3*Height) and endX - \
                #     startX > (0.01*Width) and print(endY,startY,"Height",endY-startY, endX,startX,"Width",endX-startX)

        # [3]: Sort the boundring boxes to make sure that the characters are drawin in the right order
        bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])
        # print(bounding_boxes)
        # [FIX]: avoid overlapping of contours
        accurate_bounding_box=[]
        old_endX=0
        for box in bounding_boxes:
            [Xmin, Xmax, Ymin, Ymax] = box
            if (Xmin>old_endX):
                accurate_bounding_box.append(box)
                old_endX=Xmax
                
        bounding_boxes=accurate_bounding_box
        # print(bounding_boxes)
        # [4] : Draw a Box surrounding the character
        img_with_boxes = np.copy(image)  # np.zeros(image.shape)
        # When provided with the correct format of the list of bounding_boxes, this section will set all pixels inside boxes in img_with_boxes
        for box in bounding_boxes:
            [Xmin, Xmax, Ymin, Ymax] = box
            rr, cc = sk.draw.rectangle_perimeter(
                start=(Ymin, Xmin), end=(Ymax, Xmax), shape=image.shape)
            img_with_boxes[rr, cc] = 0  # set color Black
        Xmin, Xmax, Ymin, Ymax = bounding_boxes[1]
        # show_images([img_with_boxes])
        # [5]: create a list of images cropped images for each character
        character_Image_list = []
        CHARACTER_PADDING_X: Final[int] = 2
        CHARACTER_PADDING_Y: Final[int] = 2
        for box in bounding_boxes:
            character = image_out[box[2]-CHARACTER_PADDING_Y:box[3] +
                                CHARACTER_PADDING_Y, box[0]-CHARACTER_PADDING_X:box[1]+CHARACTER_PADDING_X]
            character_Image_list.append(character)

        # show_images(character_Image_list)
        # for i in range(len(character_Image_list)):
        #     plt.subplot(1, len(character_Image_list), i+1)
        #     plt.imshow(character_Image_list[i], cmap='gray')
        #     plt.axis('off')
        # plt.show()

        # ---> List of boxes for each character
        return character_Image_list

    # [4]: Character Recognition
    def recognize_Character(self, image: np.ndarray) -> str:
        data2=""
        # show_images(chars)
        for img in image:
            # print(img)
            new_img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), interpolation = cv2.INTER_AREA)
            new_img = new_img.reshape((1,IMG_WIDTH*IMG_HEIGHT))
            # print(new_img.shape)
            y_prediction = self.knnModel.predict(new_img)
            # print(digitLetter[int(y_prediction)])
            data2+=digitLetter[int(y_prediction)]
        return data2