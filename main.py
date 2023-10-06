import cv2
import numpy
# from sys import argv

if __name__ == "__main__":
    video_file = "./Videos/test.mp4"
    

    video = cv2.VideoCapture()
    video.open(video_file)
    
    ret, frame = video.read()
    assert ret

    # Find starting bounds
    bbox = cv2.selectROI("Starting bounds", frame, False)
    cv2.destroyWindow("Starting bounds")
    tracker = cv2.TrackerCSRT.create()
    tracker.init(frame, bbox)
    
    while True:
        ret, frame = video.read()
        if not ret:
            break

        ret, bbox = tracker.update(frame)

        if ret:
            topleft = (int(bbox[0]), int(bbox[1]))
            bottomright = (int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
            center = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
            cv2.drawMarker(frame, center, (0,255,0))
            cv2.rectangle(frame, topleft, bottomright, (0,255,0))
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) == 27:
            break