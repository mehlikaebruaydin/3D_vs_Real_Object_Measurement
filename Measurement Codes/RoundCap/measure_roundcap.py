import cv2
import numpy as np
import math
import find_roundcap
from RoundCap.thickness_roundcap import roundcap_yukseklik

A4_WIDTH_CM = 13.0
h = 20
fx, fy = 0.2, 0.2  # Görsel küçültme oranı

def cap_olcum(image_path, kalinlik):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image could not be loaded: " + image_path)

    imgContour, conts = find_roundcap.getContours(img, cThr=[30, 100], minArea=1000, filter=4, draw=True)
    if len(conts) == 0:
        raise ValueError("A4 paper could not be detected.")

    biggest = conts[0][2]
    x, y, w, h_a4 = cv2.boundingRect(biggest)
    pixel_to_cm_ratio = w / A4_WIDTH_CM
    cv2.polylines(imgContour, [biggest], True, (0, 255, 0), 3)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 2)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    imgSmall = cv2.resize(imgContour, (0, 0), fx=fx, fy=fy)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            (cx, cy), radius = cv2.minEnclosingCircle(cnt)
            center = (int(cx), int(cy))
            radius = int(radius)
            diameter_px = radius * 2
            diameter_cm = round((1 / h) * (h - kalinlik) * (diameter_px / pixel_to_cm_ratio), 2)

            radius_cm = round(diameter_cm / 2, 2)
            circumference_cm = round(math.pi * diameter_cm, 2)
            thickness = round(kalinlik, 2)
            area_cm2 = round(math.pi * (radius_cm ** 2), 2)

            scaled_center = (int(center[0] * fx), int(center[1] * fy))
            scaled_radius = int(radius * fx)

            text_cap = f"Diameter: {diameter_cm:.2f} cm"
            pos_cap = (scaled_center[0] - 80, scaled_center[1] - scaled_radius - 20)
            cv2.putText(imgSmall, text_cap, (pos_cap[0] + 2, pos_cap[1] + 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(imgSmall, text_cap, pos_cap,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

            cv2.circle(imgSmall, scaled_center, scaled_radius, (0, 255, 0), 2)
            cv2.circle(imgSmall, scaled_center, 3, (0, 0, 255), -1)

            info_lines = [
                ("Radius", f"{radius_cm} cm"),
                ("Circumference", f"{circumference_cm} cm"),
                ("Thickness", f"{thickness} cm"),
                ("Area", f"{area_cm2} cm^2")
            ]

            colors = [(255, 255, 0), (0, 255, 0), (0, 128, 255), (255, 255, 255)]
            x, y = 30, 50

            for i, (label, value) in enumerate(info_lines):
                line = f"{label}: {value}"
                ypos = y + i * 60
                cv2.putText(imgSmall, line, (x + 2, ypos + 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(imgSmall, line, (x, ypos),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, colors[i], 2, cv2.LINE_AA)

            return imgSmall, diameter_cm, radius_cm, {
                "diameter": diameter_cm,
                "radius": radius_cm,
                "circumference": circumference_cm,
                "area": area_cm2,
                "thickness": thickness
            }

    raise ValueError("Daire bulunamadı.")
