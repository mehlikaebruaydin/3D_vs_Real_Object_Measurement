import cv2
import numpy as np

def yukseklik(image_path):
    cetvel = 3  # cm
    clicks = []
    fx, fy = 0.40, 0.40

    def mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(clicks) < 4:
            real_x = int(x / fx)
            real_y = int(y / fy)
            clicks.append((real_x, real_y))

    img = cv2.imread(image_path)
    if img is None:
        print("Image not found.")
        return None

    clone = img.copy()
    cv2.namedWindow("Measurement of thickness")
    cv2.setMouseCallback("Measurement of thickness", mouse_click)

    kibrit_gercek_yukseklik = None
    print("Please mark 3 cm on the ruler first. Then, select the height limits of your object.")

    while True:
        temp = clone.copy()
        for pt in clicks:
            cv2.circle(temp, pt, 15, (0, 0, 255), -1)

        if len(clicks) == 4:
            cv2.line(temp, clicks[0], clicks[1], (255, 0, 0), 2)
            cv2.line(temp, clicks[2], clicks[3], (0, 255, 0), 2)

            cetvel_pix = abs(clicks[0][1] - clicks[1][1])
            kibrit_pix = abs(clicks[2][1] - clicks[3][1])

            kibrit_gercek_yukseklik = (kibrit_pix / cetvel_pix) * cetvel

            cv2.putText(temp, f"The height of the object: {kibrit_gercek_yukseklik:.2f} cm",
                        (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

            display_img = cv2.resize(temp, (0, 0), fx=fx, fy=fy)
            cv2.imshow("Measurement of thickness", display_img)
            cv2.waitKey(3000)
            break

        display_img = cv2.resize(temp, (0, 0), fx=fx, fy=fy)
        cv2.imshow("Measurement of thickness", display_img)

        key = cv2.waitKey(1)
        if key == ord('r'):
            clicks.clear()

    cv2.destroyWindow("Measurement of thickness")
    return kibrit_gercek_yukseklik
