# scan.py by tom o'donnell
#
# uses opencv to read the stickers on a rubiks cube
# for use with a solving algorithm such as cubebot2.0
# supports calibrating colors for increased accuracy

import subprocess
from calendar import c
import math
from statistics import mean
import numpy as np
import cv2

# coordinates of centers of circles
centers = [
    [150, 75], [300, 75], [450, 75],
    [150, 225], [300, 225], [450, 225],
    [150, 375], [300, 375], [450, 375]
]

scan_to_cornerstring = [
    [0, 0], [2, 0], [5, 2], [0, 2], [4, 2], [5, 0], [0, 8], [4, 0], [3, 2], [0, 6], [2, 2], [3, 0], # top pieces
    [1, 0], [2, 8], [3, 6], [1, 2], [4, 6], [3, 8], [1, 8], [4, 8], [5, 6], [1, 6], [2, 6], [5, 8]  # bottom pieces
]
scan_to_edgestring = [
    [0, 1], [5, 1], [0, 5], [4, 1], [0, 7], [3, 1], [0, 3], [2, 1], # top pieces
    [5, 5], [2, 3], [3, 3], [2, 5], [3, 5], [4, 3], [5, 3], [4, 5],  # middle pieces
    [1, 1], [3, 7], [1, 5], [4, 7], [1, 7], [5, 7], [1, 3], [2, 7]  # bottom pieces
]

# stores calibrated colors
cal_color = [
    [], [], [], [], [], []
]

det_colors = []
confidence_metric = []
colors = ["Red", "Orange", "Blue", "Green", "White", "Yellow"]
color_to_rgb = {
    "Red": (0,0,255),
    "Orange": (0,165,255),
    "Blue": (255,0,0),
    "Green": (0,255,0),
    "White": (255,255,255),
    "Yellow": (0,255,255),
}

r = []
g = []
b = []

color = [0, 0, 0] # r, g, b
yes = (0,0,0)

faces = []

windowsize = 5
smoothing = 8

vid = cv2.VideoCapture(0)

def main():
    cald = False
    scanned_faces = 0
    while(True):
          
        # Capture the video frame
        # by frame
        ret, img = vid.read()
        #img = cv2.flip(img,0)
        yes = img.shape

        # draw circles for each center
        for center_num in range (0, len(centers)):
            cv2.circle(img, centers[center_num], 25, (0,0,255), 2)

        if cald:
            # state that we're calibrated, and also watch out for pressing "e"
            cv2.putText(img,"fully calibrated",(5,475), cv2.FONT_HERSHEY_SIMPLEX, .85, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img,"fully calibrated",(5,475), cv2.FONT_HERSHEY_SIMPLEX, .85, (255, 0, 255), 1, cv2.LINE_AA)
            for circle in range(0, len(centers)):
                read_color = scan(windowsize, img, centers[circle]) #read sticker color
                min_dist = 100000
                # find calibrated color with least euclidean distance from read color
                for col in range(0, len(cal_color)):
                    dist = color_dist(cal_color[col], read_color)
                    if dist < min_dist:
                        min_dist = dist
                        detected_color = colors[col]
                det_colors.append(detected_color)
                # max euclidean distance is 255*sqrt(3), so calculate accuracy using that
                #print(f'{detected_color} - confidence=[{round(100-((min_dist)*100)/(255*math.sqrt(3)),2)}%]')
                confidence_metric.append(round(100-((min_dist)*100)/(255*math.sqrt(3)),2))

            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord('q'):
                break
            if pressedKey == ord('e'):
                faces.append([w[0] for w in det_colors])
                scanned_faces = scanned_faces + 1

                for center_num in range (0, len(centers)):
                    cv2.circle(img, centers[center_num], 15, (255,0,255), -1)

                if scanned_faces == 6:
                    print("full scanned cube")

                    cornerstate = ""
                    edgestate = ""
                    for x in range(0, len(scan_to_cornerstring)):
                        cornerstate += faces[scan_to_cornerstring[x][0]][scan_to_cornerstring[x][1]]
                    for x in range(0, len(scan_to_edgestring)):
                        edgestate += faces[scan_to_edgestring[x][0]][scan_to_edgestring[x][1]]
                    print("detected cube: ", cornerstate, edgestate)
                    subprocess.Popen([r'CubeBot2.0.exe', 'solve', cornerstate, edgestate])
                    return()
            
            renderCube(det_colors, confidence_metric)

                
        else:
            # if not calibrated, don't need to scan the cube or check if we want to scan a side
            # basically just watch for "c" meaning to calibrate
            
            # check keys pressed
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord('q'):
                break
            if pressedKey == ord('e'):
                    faces.append([w[0] for w in det_colors])
                    print(faces)

            # calibrate colors
            if pressedKey == ord('c'):
                scan_num = 0
                while(True):
                    # need new feed of video since we are overlaying text and waiting for input
                    ret, img = vid.read()
                    #img = cv2.flip(img,0)
                    yes = img.shape

                    # draw center circle and color to scan
                    center = (int(yes[1]/2), int(yes[0]/2))
                    cv2.circle(img, center, 25, (0,0,255), 2)
                    img = cv2.putText(img,colors[scan_num],(10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5, cv2.LINE_AA)
                    img = cv2.putText(img,colors[scan_num],(10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2, cv2.LINE_AA)

                    pressedKey = cv2.waitKey(1) & 0xFF
                    if pressedKey == ord('c'):
                    # if press c again, read color and store
                        cal_color[scan_num] = scan(windowsize, img, center)
                        scan_num = scan_num + 1 # increment the color we scan
            
                    if pressedKey == ord('q') or scan_num == 6:
                        cald = True
                        break

                    cv2.imshow("Output", img)
        cv2.imshow("Output", img)
            
    vid.release()
    cv2.destroyAllWindows()


def color_dist(f, s):
    return math.sqrt( (f[0]-s[0])**2 + (f[1]-s[1])**2 + (f[2]-s[2])**2)   

def scan(windowsize, img, center):
    r.clear()
    g.clear()
    b.clear()
    # iterate in a cube window, averaging each pixel
    for x in range (center[0]-windowsize, center[0]+windowsize):
        for y in range(center[1]-windowsize, center[1]+windowsize):
            b.append(img[y][x][0])
            g.append(img[y][x][1])
            r.append(img[y][x][2])
    cv2.circle(img, center, windowsize, (0,0,255), -1)
    return (int(mean(b)), int(mean(g)), int(mean(r)))

def renderCube(colors, confidence):
    rend = np.zeros((875,875,3), dtype=np.uint8)
    ind = 0

    for y in range(0,3):
        for x in range(0,3):
            col = color_to_rgb[colors[ind]]

            cv2.rectangle(rend,(175+175*x, 175+175*y),(350+175*x,350+175*y), col, -1)

            cv2.putText(rend, f'[{confidence[ind]}%]', (205+175*x,275+175*y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.putText(rend, f'[{confidence[ind]}%]', (205+175*x,275+175*y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 150, 0), 2, cv2.LINE_AA)
            ind = ind + 1

    cv2.imshow("detect", rend)
    det_colors.clear()
    confidence_metric.clear()

if __name__ == "__main__":
    main()