import cv2
import mediapipe as mp
import numpy as np
#from .config import args, options

VERTICAL_CAMERA = 204

class ObstacleReader:

    def __init__(self):
        self.x_centers = []
        self.y_centers = []
        self.radii = []

        self.cap = cv2.VideoCapture(1)

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def detect(self):

        detected_circles = None

        while (self.cap.isOpened()):
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                return
        
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
            gray_blurred = cv2.blur(gray, (3, 3))
            print(gray.shape)
    
            detected_circles = cv2.HoughCircles(gray_blurred,  
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                       param2 = 30, minRadius = 1, maxRadius = 40) 
      
            # Draw circles that are detected. 
            if detected_circles is not None: 
      
                # Convert the circle parameters a, b and r to integers. 
                detected_circles = np.uint16(np.around(detected_circles))
      
                for pt in detected_circles[0, :]: 
                    a, b, r = pt[0], pt[1], pt[2]
                    print(a, b, r)


                    # Draw the circumference of the circle. 
                    cv2.circle(image, (a, b), r, (0, 255, 0), 2) 
                    # Draw a small circle (of radius 1) to show the center. 
                    cv2.circle(image, (a, b), 1, (0, 0, 255), 3)

                    # conversion in screen format
                    a *=2
                    b *= 3/2
                    r *= np.sqrt(3)

                    self.x_centers.append(a)
                    self.y_centers.append(b)
                    self.radii.append(r)
                    print(a, b, r)
        
            cv2.imshow("Detected Circles", image)
            return
            #if cv2.waitKey(0):
            #    cv2.destroyWindow("Detected Circles")
            #    break
