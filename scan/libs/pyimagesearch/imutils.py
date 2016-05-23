# Import the necessary packages
import numpy as np
import cv2


def translate(image, x, y):
    # Define the translation matrix and perform the translation
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # Return the translated image
    return shifted


def rotate(image, angle, center=None, scale=1.0):
    # Grab the dimensions of the image
    (h, w) = image.shape[:2]

    # If the center is None, initialize it as the center of
    # the image
    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # Return the rotated image
    return rotated


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def get_bounding_box(points):
    """
    Returns top-left, top-right, bottom-right, bottom-left coordinates of the bounding box
    of a list of points
    """
    top = 0.0
    right = 0.0
    bottom = 0.0
    left = 0.0
    for i, point in enumerate(points):
        if i == 0:
            left = point[0]
            right = point[0]
            top = point[1]
            bottom = point[1]
        else:
            if point[0] < left:
                left = point[0]
            elif point[0] > right:
                right = point[0]
            elif point[1] < bottom:
                bottom = point[1]
            elif point[1] > top:
                top = point[1]
    return np.array([[left, top], [right, top], [right, bottom], [left, bottom]])
