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

colors = ["Red", "Orange", "Blue", "Green", "White", "Yellow"]
color_to_rgb = {
    "Red": (0,0,255),
    "Orange": (0,165,255),
    "Blue": (255,0,0),
    "Green": (0,255,0),
    "White": (255,255,255),
    "Yellow": (0,255,255),
}

windowsize = 5
smoothing = 8

vid = cv2.VideoCapture(0)

def main():
    calibrated_colors = [
        [], [], [], [], [], []
    ]

    r = []
    g = []
    b = []

    scanned_faces = []
    det_colors = []
    confidence_metric = []

    calibrated = False
    scanned_faces = 0

    while(True):
        ret, img = vid.read()
        shape = img.shape

        # draw circles for each center
        for center_num in range (0, len(centers)):
            cv2.circle(img, centers[center_num], 25, (0,0,255), 2)

        if calibrated:
            read_cube_colors()

def read_cube_colors:
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
            solve_cube()
            
def solve_cube:
    cornerstate = ""
    edgestate = ""
    print("fully scanned cube")

    for x in range(0, len(scan_to_cornerstring)):
        cornerstate += faces[scan_to_cornerstring[x][0]][scan_to_cornerstring[x][1]]
        edgestate += faces[scan_to_edgestring[x][0]][scan_to_edgestring[x][1]]

    print("detected cube: ", cornerstate, edgestate)
    subprocess.Popen([r'CubeBot2.0.exe', 'solve', cornerstate, edgestate])

if __name__ == "__main__":
    main()