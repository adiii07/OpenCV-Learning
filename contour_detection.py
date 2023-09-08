import cv2
import numpy as np


def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        
        if area > 500:
            cv2.drawContours(img_contour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3: objectType = "Triangle"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4: objectType = "Circle"
            else:
                objectType = "None"
                
            cv2.rectangle(img_contour, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img_contour, objectType,
                        (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX, 
                        0.5, (0, 0, 0), 2)
                
            

path = "Resources/shapes.png"
img = cv2.imread(path)
img_contour = img.copy()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 1)
img_canny = cv2.Canny(img_blur, 50, 50)

get_contours(img_canny)

# cv2.imshow("Image", img)
# cv2.imshow("Image Gray", img_gray)
cv2.imshow("Image Blur", img_blur)
cv2.imshow("Image Contours", img_contour)
cv2.waitKey(0)