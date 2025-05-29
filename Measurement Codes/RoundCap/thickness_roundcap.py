import cv2
import numpy as np

def roundcap_yukseklik(image_path, instruction_callback=None):
    reference_length = 3.0  # 3 cm
    clicks = []
    thickness_cm = None
    window_name = "Thickness Measurement"

    img = cv2.imread(image_path)
    if img is None:
        return None

    resized = cv2.resize(img, (720, 720))
    scale_x = img.shape[1] / 720
    scale_y = img.shape[0] / 720

    def mouse_click(event, x, y, flags, param):
        nonlocal clicks
        if event == cv2.EVENT_LBUTTONDOWN and len(clicks) < 4:
            clicks.append((int(x * scale_x), int(y * scale_y)))
            if instruction_callback:
                instruction_callback(f"Clicked {len(clicks)}/4 points")

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 720, 720)
    cv2.setMouseCallback(window_name, mouse_click)

    countdown_started = False
    countdown_start_time = 0
    annotated_image = resized.copy()

    while True:
        display_img = annotated_image.copy()

        for i, (x, y) in enumerate(clicks):
            scaled = (int(x / scale_x), int(y / scale_y))
            cv2.circle(display_img, scaled, 12, (0, 255, 0), -1)
            if i % 2 == 1:
                prev = (int(clicks[i - 1][0] / scale_x), int(clicks[i - 1][1] / scale_y))
                cv2.line(display_img, prev, scaled, (0, 255, 0), 3)

        if len(clicks) == 4 and not countdown_started:
            ruler_px = np.linalg.norm(np.array(clicks[1]) - np.array(clicks[0]))
            thickness_px = np.linalg.norm(np.array(clicks[3]) - np.array(clicks[2]))

            if ruler_px < 1e-5:
                print("[ERROR] Invalid ruler length.")
                return None

            thickness_cm = round((thickness_px / ruler_px) * reference_length, 2)

            # Yazıyı doğrudan annotated_image üzerine çiz
            mid_x = int((clicks[2][0] + clicks[3][0]) / 2 / scale_x)
            mid_y = int((clicks[2][1] + clicks[3][1]) / 2 / scale_y) - 10
            text = f"thickness = {thickness_cm:.2f} cm"

            cv2.putText(annotated_image, text, (mid_x + 2, mid_y + 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4)
            cv2.putText(annotated_image, text, (mid_x, mid_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 3)

            countdown_started = True
            countdown_start_time = cv2.getTickCount()
            print(f"[INFO] Ölçüm tamamlandı: {thickness_cm:.2f} cm")

        cv2.imshow(window_name, display_img)

        if countdown_started:
            elapsed_time_ms = (cv2.getTickCount() - countdown_start_time) / cv2.getTickFrequency() * 1000
            if elapsed_time_ms >= 3000:
                break

        if cv2.waitKey(1) in [27, ord('q')]:
            break

    cv2.destroyAllWindows()
    return thickness_cm
