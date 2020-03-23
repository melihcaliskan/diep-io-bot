import cv2
import numpy as np
import time
import argparse

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 0.5
fontColor = (0, 0, 0)
lineType = 1

# NOTES
'''
If player is blue, the output will be: [227 177  69]
If player is red, the output will be: [91  89 224]
'''


def findShape(img, x, y):
    rgbimg = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    x_offset = -4
    y_offset = 12

    color = rgbimg[y+y_offset, x+x_offset]
    '''
    cv2.circle(img, (x+x_offset, y+y_offset), 2, (0, 0, 0), 1)
    cv2.putText(img,
                ("color: {}".format(color)),
                (x+30, y+40),
                font,
                fontScale,
                fontColor,
                lineType)
    '''
    print(x, y)

    '''
    cv2.putText(img, ("."), (x, y), font, 0.6, (0, 0, 0), 2)
    cv2.imshow('bu', img)
    '''
    return determine_shape_color(color)


def determine_shape_color(arr):
    print(arr)
    blue_first_range = range(40, 60)
    blue_second_range = range(100, 140)
    blue_third_range = range(50, 65)

    blue_bullet_first_range = range(195, 205)
    blue_bullet_second_range = range(188, 205)
    blue_bullet_third_range = range(38, 42)

    red_first_range = range(80, 100)
    red_second_range = range(70, 95)
    red_third_range = range(210, 240)

    yellow_first_range = range(190, 220)
    yellow_second_range = range(160, 210)
    yellow_third_range = range(30, 120)

    if(arr[0] in blue_first_range and arr[1] in blue_second_range and arr[2] in blue_third_range):
        return 'blue'
    elif(arr[0] in yellow_first_range and arr[1] in yellow_second_range and arr[2] in yellow_third_range):
        return 'yellow'
    else:
        return 'unknown'


def findPlayer(img):
    height, width, channels = img.shape
    center_x = int(width/2)
    center_y = int(height/2)
    color = img[center_y, center_x]
    return determine_player_color(color)


def determine_player_color(arr):
    blue_first_range = range(200, 250)
    blue_second_range = range(150, 190)
    blue_third_range = range(50, 85)

    red_first_range = range(80, 100)
    red_second_range = range(70, 95)
    red_third_range = range(210, 240)

    if(arr[0] in blue_first_range and arr[1] in blue_second_range and arr[2] in blue_third_range):
        return 'blue'
    elif(arr[0] in red_first_range and arr[1] in red_second_range and arr[2] in red_third_range):
        return 'red'
    else:
        return 'unknown'
