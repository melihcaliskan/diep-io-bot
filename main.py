#!/usr/bin/python3

'''
Melih Çalışkan
mlhclskn@gmail.com
19.03.2020
'''

# Window size 1148x718
# Resolution : 2880 x 1800

import threading
import time

import _thread
import cv2
import numpy as np
from helpers.findColor import findPlayer, findShape
from helpers.handleShapes import handleShapes
from helpers.moveMouse import toXY
from pynput.keyboard import Key, Listener

global player_x
global player_y

global show_contours
show_contours = False

global show_titles
show_titles = True

global follow_mouse
follow_mouse = False

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 0.5
fontColor = (0, 0, 0)
lineType = 1

# Video input
cap = cv2.VideoCapture('xxx.mp4')

# Find player color from first frame
success, image = cap.read()
player_color = findPlayer(image)

game_x_range = range(80, 1000)
game_y_range = range(40, 650)

player_x_range = range(540, 620)
player_y_range = range(330, 360)


def on_press(key):
    print('{0} pressed'.format(key))


def key_thread():
    with Listener(on_press=on_press) as listener:
        listener.join()


def handleCoordinates(org_img):
    player_x = 0
    player_y = 0

    y = 560
    x = 1030
    h = 105
    w = 105
    img = org_img[y:y+h, x:x+w]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_gray = np.array([0, 0, 0], np.uint8)
    upper_gray = np.array([255, 255, 60], np.uint8)
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

    sigma = 0.35
    v = np.median(mask_gray)
    low = int(max(0, (1.0 - sigma) * v))
    high = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(mask_gray, low, high)

    (cnts, _) = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        x_i, y_i, w, h = cv2.boundingRect(cnts[0])

        player_x = x_i
        player_y = y_i

    cv2.imshow('xy', mask_gray)
    cv2.waitKey(1)
    return [player_x, player_y]


locations = []


def handleMove(img, location):
    direction = None
    curr_x = 0
    curr_y = 0

    locations.append([location[0], location[1]])

    # If we have 2 items, we can compare them. We don't need any more.
    if len(locations) == 2:
        print(locations)

        # Current and before locations of [X,Y]
        bfr_x = locations[0][0]
        bfr_y = locations[0][0]
        curr_x = locations[1][0]
        curr_y = locations[1][1]

        if bfr_x < curr_x:
            if bfr_y < curr_y:
                direction = "north east"
            else:
                direction = "south west"

        elif bfr_x > curr_x:
            if bfr_y < curr_y:
                direction = "north eeast"
            else:
                direction = "south west"

        else:
            if bfr_y < curr_y:
                direction = "east"
            elif bfr_y > curr_y:
                direction = "west"
            else:
                direction = "same"
        locations.remove(locations[0])

    return direction


def main():
    player_x = 0
    player_y = 0
    while(cap.isOpened()):
        ret, img = cap.read()
        height, width, channels = img.shape

        img_orig = img.copy()
        if not ret:
            break

        player_location = handleCoordinates(img)
        direction = handleMove(img, player_location)
        print(direction)

        cv2.putText(img,
                    ("map location: {},{}".format(
                        player_location[0], player_location[1])),
                    (950, 470),
                    font,
                    0.6,
                    (0, 0, 0),
                    2)
        cv2.putText(img,
                    ("direction : {}".format(direction)),
                    (950, 520),
                    font,
                    0.6,
                    (0, 0, 0),
                    2)

        print("-------------")

        # Convert the color image into grayscale
        grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find edges in the image using canny edge detection method
        # Calculate lower threshold and upper threshold
        sigma = 0.35
        v = np.median(grayScale)
        low = int(max(0, (1.0 - sigma) * v))
        high = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(grayScale, low, high)

        # After finding edges we have to find contours
        # Contour is a curve of points with no gaps in the curve
        # It will help us to find location of shapes
        (cnts, _) = cv2.findContours(
            edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            x_i, y_i, w, h = cv2.boundingRect(c)

            approx = cv2.approxPolyDP(c, 0.03*cv2.arcLength(c, True), True)

            # Show or hide contours
            if(show_contours):
                cv2.drawContours(img, [approx], 0, (100, 100, 100), 2)

            # If object larger than 10x10
            if(w > 10 and h > 10 and x_i in game_x_range and y_i in game_y_range):
                x = approx.ravel()[0]
                y = approx.ravel()[1]

                # Update player info
                if(x in player_x_range and y in player_y_range):
                    player_x = x
                    player_y = y

                side_count = len(approx)

                # Show or hide titles
                if(show_titles):
                    handleShapes(img, x, y, side_count, player_color)

                if side_count == 4:
                    player_x_lower_range = range(player_x - 200, player_x+200)
                    player_y_lower_range = range(player_y - 200, player_y+200)

                    if(x in player_x_lower_range and y in player_y_lower_range):
                        player_x = x
                        player_y = y

                        cv2.putText(img,
                                    ("enemy"),
                                    (x, y-25),
                                    font,
                                    0.7,
                                    (60, 60, 180),
                                    2)

                        cv2.putText(img,
                                    ("mouse location: {},{}".format(x, y)),
                                    (int(x), int(y)),
                                    font,
                                    0.7,
                                    (0, 0, 0),
                                    2)

                        # Move cursor to enemy
                        if(follow_mouse):
                            toXY(x, y)

                if(side_count > 5 and x not in player_x_range and y not in player_y_range):
                    cv2.putText(img,
                                ("bullet"),
                                (x, y-25),
                                font,
                                0.7,
                                (250, 130, 50),
                                2)
        cv2.imshow('original', img)
        cv2.waitKey(1)


main()
