import cv2


if __name__ == "__main__":
    video_file = "Pro"
    write_file = "Pro"
    manual_input = True

    video = cv2.VideoCapture()
    video.open(f"./Videos/{video_file}.mp4")


    fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(f"./Data/{write_file}.mp4", fourcc=fourcc, fps=fps, frameSize=frame_size)
    print(f"{fps=}")
    path = []
    cv2.namedWindow("Starting bounds", cv2.WINDOW_NORMAL)
    framenum = 0
    # Find starting bounds
    while True:
        ret, frame = video.read()
        framenum += 1
        assert ret
        cv2.imshow("Starting bounds", frame)
        if cv2.waitKey(10000) not in [32, -1]:
            break
    bbox = cv2.selectROI("Starting bounds", frame, False)
    print(f"starting: {bbox=}, {framenum=}")
    cv2.destroyWindow("Starting bounds")
    tracker = cv2.TrackerCSRT.create()
    tracker.init(frame, bbox)
    
    cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        framenum+=1

        ret, bbox = tracker.update(frame)

        if ret:
            topleft = (int(bbox[0]), int(bbox[1]))
            bottomright = (int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
            center = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
            cv2.drawMarker(frame, center, (0,255,0))
            cv2.rectangle(frame, topleft, bottomright, (0,255,0))
            path.append((framenum,center))
            for (_, c1), (_, c2) in zip(path[:-1], path[1:]):
                cv2.line(frame, c1, c2, (0,255,0))
        cv2.putText(frame, f"{framenum}",center,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
        cv2.imshow("Tracking", frame)
        out.write(frame)
        if manual_input:
            i = cv2.waitKey(10000)
            if i == 32:
                continue
            elif i == 27:
                break
            else:
                bbox = cv2.selectROI("Tracking", frame)
                if bbox:
                    tracker.init(frame, bbox)
                    c = (int(bbox[0]+bbox[2]/2), int(bbox[1]+bbox[3]/2))
                    path[-1] = framenum, c
        if cv2.waitKey(1) == 27:
            break
    print(f"ended on {framenum}")
    print(path)

    with open(f"./Data/{write_file}.txt", "w") as f:
        f.write(f"{fps=}\n")
        f.write(str(path))
    out.release()