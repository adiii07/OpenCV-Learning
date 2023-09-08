import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])

while True:
    ret, frame = cap.read()
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # getting red color in the frame
    lower_range = np.array([136, 87, 111], np.uint8)
    upper_range = np.array([180, 255, 255], np.uint8)
    mask = cv2.inRange(hsv_img, lower_range, upper_range)
    
    kernel = np.ones((5, 5), "uint8")
    mask = cv2.dilate(mask, kernel)
    color_image = cv2.bitwise_and(frame, frame, mask=mask)
    
    
    contours, hierarchy = cv2.findContours(mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
      
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        if(area > 1000):
            
            approx = cv2.approxPolyDP(contour, 0.0095 * cv2.arcLength(contour, True), True)
            
            # checking for objects with 7 contours in the frame
            if len(approx) == 7:
                cv2.drawContours(frame, [approx], 0, (200, 0, 255), 5)
                
                # getting longest contour
                n = approx.ravel() 
                i = 0
            
                # bottom1_coordx = 0
                # bottom1_coordy = 0
                # bottom2_coordx = 0
                # bottom2_coordy = 0
                
                for j in n :
                    if(i % 2 == 0):
                        x = n[i]
                        y = n[i + 1]
            
                        # String containing the co-ordinates.
                        string = str(x) + " " + str(y) 
            
                        if i == 3:
                            # text on topmost co-ordinate.
                            cv2.putText(frame, "Arrow tip", (x, y),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0)) 
                            tip_coord_x = x
                            tip_coord_y = y
                            
                        
                        else:
                            # text on remaining co-ordinates.
                            cv2.putText(frame, string, (x, y), 
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0)) 
                    i = i + 1
                
                # getting the longest contour
                max_contour = max(contours, key = cv2.contourArea)
                # M = cv2.moments(max_contour)
                
                # if M['m00'] >= 0 and cv2.contourArea(max_contour) >= 2000:
                #     max_cx = int(M['m10'] / M['m00'])
                #     max_cy = int(M['m01'] / M['m00'])
                
                # cv2.line(frame, ())

                
                x,y,w,h = cv2.boundingRect(max_contour)
                
                # arrow_bot_x = tip_coord_x + 

                # draw the biggest contour (c) in green
                # cv2.line(frame, (x, y),(x, y+h), (0, 255, 0), 2)
            
              
    
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()