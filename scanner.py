"""
Scanner class that contains the logic for scanning an image
"""

from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import cv2


class Scanner:
    def __init__(self):
        pass

    @classmethod
    def scan(cls, filepath):
        print("Starting scan")
        # load the image and compute the ratio of the old height
        # to the new height, clone it, and resize it
        image = cv2.imread(filepath)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        screenCnt = None

        # loop over the contours
        for c in cnts:
            # approximate contours
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        # Check if we found a 4 point contour. If not, we create our own bounding box
        # with the largest contour
        if screenCnt is None:
            height, width, channels = image.shape
            imageBounds = np.array([[1, 1], [width, 1], [width, height], [1, height]])
            screenCnt = imutils.get_bounding_box(imageBounds)

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        warped = threshold_adaptive(warped, 250, offset=10)
        warped = warped.astype("uint8") * 255

        # Write out image to tmp file
        filename = "tmp/tmp-result.png"
        cv2.imwrite(filename, warped)
        print("Finished scan")
        return filename

