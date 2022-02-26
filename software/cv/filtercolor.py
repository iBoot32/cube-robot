from random import gauss
import numpy as np
from statistics import mean
import cv2

vid = cv2.VideoCapture(1)
windowsize = 10
det_colors = []
colors = ["Red", "Orange", "Blue", "Green", "White", "Yellow"]
cal_color = [
    [], [], [], [], [], []
]

r =[]
b = []
b = []

def main():
    while(True):
          
        # Capture the video frame
        # by frame
        ret, img = vid.read()
        img = cv2.flip(img,1)
        yes = img.shape

        # gaussian blur image
        img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0)

        calibrateColors()

        # filter using canny edge detection, find contours in canny image
        edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=100)
        contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv2.contourArea)
        contourImg = cv2.drawContours(img, contour, -1, (0,255,0), 3)
        
        cv2.imshow("contours", contourImg)


        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()

def calibrateColors():
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

if __name__ == "__main__":
    main()