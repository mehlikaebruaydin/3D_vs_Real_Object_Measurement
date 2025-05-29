import cv2
import numpy as np

def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)

    if showCanny:
        cv2.imshow('Canny', imgThre)

    contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > minArea:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append((len(approx), area, approx, cnt))
            else:
                finalContours.append((len(approx), area, approx, cnt))

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[3], -1, (0, 255, 0), 3)

    return img, finalContours


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    diff = np.diff(myPoints, axis=1)

    newPoints[0] = myPoints[np.argmin(add)]     # top-left
    newPoints[3] = myPoints[np.argmax(add)]     # bottom-right
    newPoints[1] = myPoints[np.argmin(diff)]    # top-right
    newPoints[2] = myPoints[np.argmax(diff)]    # bottom-left

    return newPoints


def warpImg(img, points, w, h, pad=20):
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    imgWarp = imgWarp[pad:imgWarp.shape[0] - pad, pad:imgWarp.shape[1] - pad]
    return imgWarp


def findDis(pts1, pts2):
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5


def drawObject(img, points, thickness=2):
    cv2.line(img, tuple(points[0][0]), tuple(points[1][0]), (255, 0, 255), thickness)
    cv2.line(img, tuple(points[1][0]), tuple(points[2][0]), (255, 0, 255), thickness)
    cv2.line(img, tuple(points[2][0]), tuple(points[3][0]), (255, 0, 255), thickness)
    cv2.line(img, tuple(points[3][0]), tuple(points[0][0]), (255, 0, 255), thickness)
