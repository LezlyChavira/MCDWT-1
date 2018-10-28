from math import log
import numpy as np
import cv2
from time import time
import sys

class WebCam():

    def process(self, frame):        
        return frame

    def run(self):
        cap = cv2.VideoCapture(0)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        n_labels = width * height * 3
        fps = cap.get(cv2.CAP_PROP_FPS)
        sys.stdout.write("Capturing from webcam at " + str(width) + 'x' + str(height) + " pixels, " + str(fps) + " Hz\n")

        counter = 0
        start = time()
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Process the frame
            frame = self.process(frame)

            # Display the resulting frame
            cv2.imshow('WebCam', frame)

            # Compute some stats on processed frame
            end = time()
            fps = counter/(end - start)
            counter += 1
            value, counts = np.unique(frame, return_counts=True)
            probs = counts / n_labels
            ent = 0.
            for i in probs:
                ent -= i * log(i, 2.0)
            sys.stdout.write("Frame={:04d} FPS={:2.1f} Entropy={:1.1f}\r".format(counter, fps, ent))
            sys.stdout.flush()

            # Exit?
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    driver = WebCam()
    driver.run()
