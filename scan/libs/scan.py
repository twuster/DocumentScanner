# USAGE
# python scan.py --image images/page.jpg 

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
                help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
# cv2.imshow("Image", image)
# cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
image, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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

# import pdb; pdb.set_trace()


# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
# cv2.imshow("Outline", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 250, offset=10)
warped = warped.astype("uint8") * 255

# show the original and scanned images
print("STEP 3: Apply perspective transform")
# cv2.imshow("Original", imutils.resize(orig, height=650))
# cv2.imshow("Scanned", imutils.resize(warped, height=650))
# cv2.waitKey(0)

print("STEP 4: Writing image")
filename = os.path.basename(args["image"])
if not os.path.exists("results"):
    os.mkdir("results")
cv2.imwrite(os.path.join("results", filename), warped)
