"""
Example script using PyOpenPose.
"""
import argparse
from libs import pyopenpose as op
import time
import cv2
import os

OPENPOSE_ROOT = os.environ["OPENPOSE_ROOT"]

def run():
    cap = cv2.VideoCapture(args.filename)
    params = dict()
    params["model_folder"] = OPENPOSE_ROOT + os.sep + "models" + os.sep
    params["face"] = True
    params["hand"] = True

    #op = OP.OpenPose((656, 368), (368, 368), (1280, 720), "COCO", OPENPOSE_ROOT + os.sep + "models" + os.sep, 0,
    #                  False, OP.OpenPose.ScaleMode.ZeroToOne, with_face, with_hands)

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    paused = False
    delay = {True: 0, False: 1}
    count = 0
    print("Entering main Loop.")

    datum = op.Datum()

    while True:
        try:
            _, frame = cap.read()

        except Exception as e:
            print("Failed to grab", e)
            break

        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])

        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        # print("Face keypoints: \n" + str(datum.faceKeypoints))
        # print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        # print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

        persons = datum.poseKeypoints

        if persons is None:
            print("No Person")
            continue
        try:
            if persons is not None and len(persons) > 1:
                print("Person > 1 ", persons[0].shape)
                continue
        except TypeError:
            continue

        gray = cv2.cvtColor(datum.cvOutputData-datum.cvInputData, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        cv2.imshow("OpenPose result", binary)
        count += 1
        print(count)
        #if count < 155 or (count > 855 and count < 1255) or (count > 1745 and count < 1775) or (count > 2225 and count < 2265) or (count > 2535 and count < 2915):
        #    continue
        #if count > 2405:
        #    break
        cv2.imwrite("original/{}.png".format(count), datum.cvOutputData)
        cv2.imwrite("landmarks/{}.png".format(count), binary)

        key = cv2.waitKey(delay[paused])
        if key & 255 == ord('p'):
            paused = not paused

        if key & 255 == ord('q'):
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='filename', type=str, help='Name of the video file.')
    args = parser.parse_args()
    if not os.path.exists(os.path.join('./', 'original')):
        os.makedirs(os.path.join('./', 'original'))
    if not os.path.exists(os.path.join('./', 'landmarks')):
        os.makedirs(os.path.join('./', 'landmarks'))
    # os.makedirs('original', exist_ok=True)
    # os.makedirs('landmarks', exist_ok=True)
    run()