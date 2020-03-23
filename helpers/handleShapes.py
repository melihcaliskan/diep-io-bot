import cv2
from helpers.findColor import findPlayer, findShape

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 0.5
fontColor = (0, 0, 0)
lineType = 1

player_x_range = range(540, 620)
player_y_range = range(330, 360)


def handleShapes(img, x, y, side_count, player_color):
    #rgbimg = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    #tmp = rgbimg[y+12, x+7]

    color = findShape(img, x, y)

    print(color)
    print("----")

    if side_count == 3:
        cv2.putText(img,
                    "triangle",
                    (x+30, y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)
    if side_count == 4:
        cv2.putText(img,
                    ("rectangle, {}".format(color)),
                    (x+30, y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)
    elif side_count == 5:
        color = findShape(img, x, y)
        print(color)
        cv2.putText(img,
                    ("pentagon, {}".format(color)),
                    (x+30, y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)
    elif side_count > 5:
        text = "circle"
        if(x in player_x_range and y in player_y_range):
            cv2.putText(img,
                        ("Player, {}".format(player_color)),
                        (x, y-30),
                        font,
                        0.6,
                        fontColor,
                        2)
        else:
            cv2.putText(img,
                        "circle",
                        (x+30, y),
                        font,
                        fontScale,
                        fontColor,
                        lineType)

    # If it is a helpful shape write coordinates of it.
    if(side_count == 3 or side_count == 4 or side_count == 5):
        cv2.putText(img,
                    ("{},{}".format(x, y)),
                    (x+30, y+20),
                    font,
                    fontScale,
                    fontColor,
                    lineType)

    # If x and y in range, we have coordinates of player.
    if(x in player_x_range and y in player_y_range):
        player_x = x
        player_y = y

        # Player info
        cv2.putText(img,
                    ("Player location: {},{}".format(player_x, player_y)),
                    (20, 500), font, 0.6, (0, 0, 0), 2)
        cv2.putText(img,
                    ("Player color: {}".format(player_color)),
                    (20, 530), font, 0.6, (0, 0, 0), 2)

        # Circle around the player
        cv2.circle(img, (x+18, y+10), 220, (55, 55, 180), 4)
        cv2.putText(img, ("r=110"), (x, y+170),
                    font, 0.6, (0, 0, 0), 2)
