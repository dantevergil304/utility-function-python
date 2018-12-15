import cv2
import os
import errno


def getTotalFrame(path):
    # calculate the total frames of a video
    cap = cv2.VideoCapture(path)
    cnt = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is False:
            break
        cnt += 1
    return cnt


def getDuration(cap):
    # duration = total_frame / FPS
    return cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)


def KeyframeExtraction(path, sampling_rate=None):
    # path: path to video file
    # sampling_rate: the number of frames per second
    cap = cv2.VideoCapture(path)

    total_frame = getTotalFrame(path)
    duration = getDuration(cap)
    fps = total_frame / duration
    coef = round(fps / sampling_rate)

    filename = path.split('/')[-1]
    directory_path = './keyframes/' + filename.split('.')[0] + '/'
    print('...Extracting frames to ' + directory_path)
    try:
        os.makedirs(directory_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    index = 0
    label = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret is True:
            if (index % coef == 0) or (sampling_rate is None):
                cv2.imwrite(directory_path + filename.split('.')[0] + '-KF'
                            + str(label).zfill(5) + '.jpg', frame)
                label += 1
        else:
            break
        index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    KeyframeExtraction('./videos/29_11_2017 06_13_59 (UTC+07_00).mkv', 5)
