from flock.reader import Reader
import cv2

def list_cameras(max_tested=10):

    available_cameras = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    print(available_cameras)

#list_cameras()
obs = Reader()
obs.detect()
if cv2.waitKey(0):
    cv2.destroyWindow("Detected Circles")
obs.quit()
