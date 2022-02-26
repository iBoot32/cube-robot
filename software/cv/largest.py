from random import gauss
import numpy as np
import cv2

vid = cv2.VideoCapture(1)
def main():
    while(True):
          
        # Capture the video frame
        # by frame
        ret, img = vid.read()
        img = cv2.flip(img,1)
        yes = img.shape

        # gaussian blur image
        img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0)

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

if __name__ == "__main__":
    main()