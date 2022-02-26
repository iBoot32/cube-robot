from statistics import mean
import math
from turtle import color
import numpy as np
import cv2

pix = [
    [200,20], [222,20], [246,20],
    [180,45], [202, 45], [224, 45], [246,45], [268, 45],
    [180,70], [202, 70], [224, 70], [246,70], [268, 70],
    [180,95], [202, 95], [224, 95], [246,95], [268, 95],
    [200,110], [222,110], [246,110],
]

det_colors = []
colors = ["Red", "Orange", "Blue", "Green", "White", "Yellow"]

rgb = [ 
    [0,0,238], [0,161,255], [242,0,0], [0,216,0], [255,255,255], [0,254,254]
]

readPix = []
r = []
g = []
b = []

def main():
    min_dist = 100000
    img = cv2.imread("read.png", cv2.IMREAD_COLOR)
    dim = img.shape
    while (pix[19][1]+30 < dim[0]):
        print(dim[0])
        print(pix[19][1])
        for x in range(0, len(pix)):
            img = cv2.circle(img, pix[x], 1, (255,255,255), 1)
            cv2.imshow("ye", img)

            min_dist = 1000000
            # for each pixel on one cube, read the color
            readPix.append(scan(5, img, pix[x]))
            for i in range(0, len(rgb)):
                dist = color_dist(readPix[x], rgb[i])
                if dist < min_dist:
                    min_dist = dist
                    det_col = rgb[i]
                    dett = colors[i]
            print(f'{readPix[x]} closest to {det_col} which is {dett}')
        for p in range(0, len(pix)):
            pix[p][1] = pix[p][1] + 130 # add 30 to y value so next loop we read the next cube down
    cv2.waitKey(0)

def color_dist(f, s):
    return math.sqrt( (f[0]-s[0])**2 + (f[1]-s[1])**2 + (f[2]-s[2])**2) 

def scan(windowsize, img, center):
    r.clear()
    g.clear()
    b.clear()
    for x in range (center[0]-windowsize, center[0]+windowsize):
        for y in range(center[1]-windowsize, center[1]+windowsize):
            b.append(img[y][x][0])
            g.append(img[y][x][1])
            r.append(img[y][x][2])
    cv2.circle(img, center, windowsize, (0,0,255), -1)
    return (int(mean(b)), int(mean(g)), int(mean(r)))

if __name__ == "__main__":
    main()