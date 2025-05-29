import cv2
from Matchbox import find_matchbox


def kibrit_olc(top_path, kalinlik):
    scale = 3
    wP = 130 * scale
    hP = 210 * scale
    h = 25

    img = cv2.imread(top_path)
    imgContour, conts = find_matchbox.getContours(img, cThr=[30, 100], minArea=5000, filter=0, draw=False)
    if len(conts) == 0:
        print("Object contour not found.")
        return None, None, None

    biggest = conts[0][2]
    imgWarp = find_matchbox.warpImg(img, biggest, wP, hP)

    _, conts2 = find_matchbox.getContours(imgWarp, cThr=[81, 121], minArea=1000, filter=4, draw=False)
    if len(conts2) == 0:
        print("İç konturlar bulunamadı.")
        return None, None, None

    obj = conts2[0]
    nPoints = find_matchbox.reorder(obj[2])
    nW = round((find_matchbox.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 2)
    nH = round((find_matchbox.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 2)

    gw = (1 / h) * (h - kalinlik) * nW
    gh = (1 / h) * (h - kalinlik) * nH
    gwy = round(gw, 2)
    ghy = round(gh, 2)

    # Çizimleri imgWarp üzerinde yap
    x, y, w, h_box = cv2.boundingRect(obj[2])

    cv2.arrowedLine(imgWarp, tuple(nPoints[0][0]), tuple(nPoints[1][0]), (255, 0, 255), 3, 8, 0, 0.05)
    cv2.arrowedLine(imgWarp, tuple(nPoints[0][0]), tuple(nPoints[2][0]), (255, 0, 255), 3, 8, 0, 0.05)

    cv2.putText(imgWarp, f'{gwy:.2f}cm', (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                (255, 0, 255), 2)
    cv2.putText(imgWarp, f'{ghy:.2f}cm', (x - 70, y + h_box // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                (255, 0, 255), 2)

    # Kalınlık yazısı (üstte)
    cv2.putText(imgWarp, f"thickness = {kalinlik:.2f} cm", (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

    return imgWarp, gwy, ghy
