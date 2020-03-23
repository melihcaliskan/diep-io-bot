from pynput.mouse import Button, Controller
import time

mouse = Controller()

HEADER_HEIGHT = 65


def moveRight():
    mouse.position = (mouse.position[0]+20, mouse.position[1])


def moveLeft():
    mouse.position = (mouse.position[0]-20, mouse.position[1])


def moveTop():
    mouse.position = (mouse.position[0], mouse.position[1]-20)


def moveBottom():
    mouse.position = (mouse.position[0], mouse.position[1]+20)


def toRight():
    mouse.position = (1500, 500)


def toLeft():
    mouse.position = (600, 500)


def toXY(x, y):
    mouse.position = (x, y+HEADER_HEIGHT)
    print(mouse.position)
    '''
    # Move with ease
    tmp_mouse = (mouse.position[0], mouse.position[1])
    print(x, y, tmp_mouse)
    while x > tmp_mouse[0]:
        while y > tmp_mouse[1]:
            mouse.position = (tmp_mouse[0]-20, tmp_mouse[1]-20)
    while x > tmp_mouse[0]:
        while y < tmp_mouse[1]:
            mouse.position = (tmp_mouse[0]-20, tmp_mouse[1]+20)

    while x < tmp_mouse[0]:
        while y > tmp_mouse[1]:
            mouse.position = (tmp_mouse[0]+20, tmp_mouse[1]-20)
    while x < tmp_mouse[0]:
        while y < tmp_mouse[1]:
            mouse.position = (tmp_mouse[0]+20, tmp_mouse[1]+20)
    '''


def toWindow():
    mouse.position = (600, 600)
    mouse.press(Button.left)
    mouse.release(Button.left)
    print("Move back to window")
