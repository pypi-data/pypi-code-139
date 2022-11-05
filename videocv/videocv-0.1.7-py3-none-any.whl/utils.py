import cv2
import numpy as np
from videocv.video import Video


def check_keyinput(video: Video):
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        return True
    elif key > 47 and key < 58:
        num = key - 48
        pos = num * video.frame_count // 10
        video.set_pos(pos)
        video()
    elif key == ord(" "):
        key = cv2.waitKey(0)
    elif key == ord("a"):
        video.move(-1)
    elif key == ord("s"):
        video.move(+1)
    elif key == ord("z"):
        video.move(-100)
    elif key == ord("x"):
        video.move(+100)


def show_status(video: Video):
    f, F = video.get_pos(), video.frame_count
    shape = (32, 480, 3)
    progress_bar = np.zeros(shape, dtype=np.uint8)
    x = int(f / F * shape[1])
    cv2.line(progress_bar, (x, 0), (x, shape[0]), (0, 255, 0), 1)

    shape = (100, 480, 3)
    view = np.zeros(shape, dtype=np.uint8)
    logs = [
        "(W, H) = (%d, %d)" % (video.size[0], video.size[1]),
        "Frame = %d / %d" % (f, F),
        "Video FPS: %f" % video.fps,
        "Play FPS: %f" % (1 / video.latency),
    ]
    p = [5, 20]
    for log in logs:
        cv2.putText(view, log, p, 0, 0.5, (0, 255, 255), 1)
        p[1] += 20

    status = np.concatenate([progress_bar, view], axis=0)
    cv2.imshow("status", status)
